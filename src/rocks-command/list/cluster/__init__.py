# $Id: __init__.py,v 1.4 2008/09/08 21:51:40 bruno Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		            version 5.0 (V)
# 
# Copyright (c) 2000 - 2008 The Regents of the University of California.
# All rights reserved.	
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 
# 1. Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright
# notice unmodified and in its entirety, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided 
# with the distribution.
# 
# 3. All advertising and press materials, printed or electronic, mentioning
# features or use of this software must display the following acknowledgement: 
# 
# 	"This product includes software developed by the Rocks(r)
# 	Cluster Group at the San Diego Supercomputer Center at the
# 	University of California, San Diego and its contributors."
# 
# 4. Except as permitted for the purposes of acknowledgment in paragraph 3,
# neither the name or logo of this software nor the names of its
# authors may be used to endorse or promote products derived from this
# software without specific prior written permission.  The name of the
# software includes the following terms, and any derivatives thereof:
# "Rocks", "Rocks Clusters", and "Avalanche Installer".  For licensing of 
# the associated name, interested parties should contact Technology 
# Transfer & Intellectual Property Services, University of California, 
# San Diego, 9500 Gilman Drive, Mail Code 0910, La Jolla, CA 92093-0910, 
# Ph: (858) 534-5815, FAX: (858) 534-7345, E-MAIL:invent@ucsd.edu
# 
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS''
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# @Copyright@
#
# $Log: __init__.py,v $
# Revision 1.4  2008/09/08 21:51:40  bruno
# added optional status columns to VM listing commands
#
# Revision 1.3  2008/09/04 19:55:00  bruno
# list the FQDN for frontends
#
# Revision 1.2  2008/08/22 23:25:56  bruno
# closer
#
# Revision 1.1  2008/08/21 21:41:36  bruno
# list physical and virtual clusters
#

import rocks.vm
import rocks.commands

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.list.command):

	"""
	Lists a cluster, that is, for each frontend, all nodes that are
	associated with that frontend are listed.
	
	<arg optional='1' type='string' name='cluster' repeat='1'>
	Zero, one or more frontend names. If no frontend names are supplied,
	information for all clusters will be listed.
	</arg>

	<param type='bool' name='status'>
	If true, then for each VM-based cluster node, output the VM's status
	(e.g., 'active', 'paused', etc.).
        </param>

	<example cmd='list cluster frontend-0-0'>
	List the cluster associated with the frontend named 'frontend-0-0'.
	</example>

	<example cmd='list cluster'>
	List all clusters.
	</example>
	"""

	def getStatus(self, hosts):
		vm = rocks.vm.VM(self.db)
		vm_status = {}

		#
		# get a list of all the physical hosts
		#
		physhosts = []
		for host in self.getHostnames():
			if not vm.isVM(host):
				physhosts.append(host)

		#
		# get the status for all running VMs
		#
		hostindex = -6
		stateindex = -2
		self.vm_status = {}

		output = self.command('run.host', physhosts +
			[ '/usr/sbin/xm list' ] )

		for line in output.split('\n'):
			if len(line) < 1:
				continue 

			l = line.split()

			if len(l) > 5:
				h = None

				#
				# we need this loop because when a VM is
				# migrating or saved, it changes the
				# name of the VM to 'migrating-<hostname>'.
				# this loop finds the hostname for the VM (if
				# it running).
				#
				for host in hosts:
					if l[hostindex] in host:
						h = host
						break

				if not h:
					continue

				state = []
				#
				# a 'blocked' VM can be one that is waiting
				# for I/O or has gone to sleep. let's call it
				# 'active', because the VM is running, it just
				# isn't active.
				#
				if 'r' in l[stateindex] or 'b' in l[stateindex]:
					state.append('active')
				if 'p' in l[stateindex]:
					state.append('paused')
				if 's' in l[stateindex]:
					state.append('shutdown')
				if 'c' in l[stateindex]:
					state.append('crashed')
				if 'd' in l[stateindex]:
					state.append('dying')

				comma = ','
				vm_status[h] = comma.join(state)

		return vm_status


	def getClientInfo(self, host, showstatus):
		info = ('', host, 'VM')

		if showstatus:
			status = None
			if self.vm_status.has_key(host):
				status = self.vm_status[host]
				info += (status,)
		
		return info


	def run(self, params, args):
		(showstatus, ) = self.fillParams( [ ('status', 'n') ])
		showstatus = self.str2bool(showstatus)

		frontends = self.getHostnames( [ 'frontend' ])

		if len(args) > 0:
			hosts = self.getHostnames(args)
			for host in hosts:
				if host not in frontends:
					self.abort('host %s is not a frontend'
						% host)
		else:
			hosts = frontends

		vm = rocks.vm.VM(self.db)

		if showstatus:
			#
			# get a list of all the VMs
			#
			vmhosts = []
			for host in self.getHostnames():
				if vm.isVM(host):
					vmhosts.append(host)

			self.vm_status = self.getStatus(vmhosts)

		self.beginOutput()

		for frontend in hosts:
			#
			# get the FQDN of the frontend
			#
			rows = self.db.execute("""select net.name from
				nodes n, networks net, subnets s where 
				s.name = 'public' and s.id = net.subnet
				and n.name = '%s' and n.id = net.node"""
				% (frontend))

			if rows == 1:
				fqdn, = self.db.fetchone()
			else:
				fqdn = ''

			if vm.isVM(frontend):
				info = (fqdn, '', 'VM')
				if showstatus:
					status = None
					if self.vm_status.has_key(frontend):
						status = self.vm_status[frontend]
					info += (status,)
		
				self.addOutput(frontend, info)

				#
				# all client nodes of this VM frontend have
				# the same vlan id as this frontend
				#
				rows = self.db.execute("""select
					net.vlanid from
					networks net, nodes n, subnets s where
					n.name = '%s' and net.node = n.id and
					s.name = 'private' and
					s.id = net.subnet""" % frontend)

				if rows > 0:
					vlanid, = self.db.fetchone()
				else:
					self.abort('could not find Vlan Id ' +
						'for frontend %s' % frontend)

				rows = self.db.execute("""select n.name from
					networks net, nodes n where
					net.vlanid = %s and net.node = n.id
					""" % vlanid)

				for client, in self.db.fetchall():
					if client != frontend and \
						vm.isVM(client):

						info = self.getClientInfo(
							client, showstatus)
		
						self.addOutput('', info)
			else:
				info = (fqdn, '', 'physical')
				if showstatus:
					info += (None,)
		
				self.addOutput(frontend, info)

				#
				# a physical frontend. go get all the physical
				# client nodes
				#
				clients = self.getHostnames()

				for client in clients:
					if client not in frontends and \
						not vm.isVM(client):
		
						info = ('',client, 'physical')
						if showstatus:
							info += (None,)

						self.addOutput('', info)

		header = [ 'frontend', 'FQDN', 'client nodes', 'type' ]
		if showstatus:
			header.append('status')

		self.endOutput(header, trimOwner = 0)

