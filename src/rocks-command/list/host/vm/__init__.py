# $Id: __init__.py,v 1.8 2008/09/08 21:27:43 bruno Exp $
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
# Revision 1.8  2008/09/08 21:27:43  bruno
# add optional status to 'rocks list host vm'
#
# Revision 1.7  2008/04/21 16:37:35  bruno
# nuked the vm_macs table -- now using the networks table to store/retrieve
# mac addresses for VMs
#
# Revision 1.6  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.5  2008/02/27 01:29:27  bruno
# bug fix
#
# Revision 1.4  2008/02/19 23:20:24  bruno
# katz made me do it.
#
# Revision 1.3  2008/02/07 20:08:24  bruno
# retooled the commands and database tables to handle moving running VMs
#
# Revision 1.2  2008/01/30 22:01:34  bruno
# closer
#
# Revision 1.1  2007/12/03 19:48:51  bruno
# xen for V
#
#

import os.path
import rocks.commands
import rocks.vm

class Command(rocks.commands.list.host.command):
	"""
	Lists the VM configuration for hosts.
	
	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied,
	information for all hosts will be listed.
	</arg>

	<param type='bool' name='showdisks'>
	If true, then output VM disk configuration. The default is 'false'.
        </param>

	<param type='bool' name='status'>
	If true, then output each VM's status (e.g., 'active', 'paused', etc.).
        </param>

	<example cmd='list host vm compute-0-0'>
	List the VM configuration for compute-0-0.
	</example>

	<example cmd='list host vm compute-0-0 compute-0-1'>
	List the VM configuration for compute-0-0 and compute-0-1.
	</example>
	"""

	def getStatus(self, args, hosts):
		vm = rocks.vm.VM(self.db)

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
		vm_status = {}

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


	def run(self, params, args):
		(showdisks, showstatus) = self.fillParams( [
			('showdisks', 'n'), 
			('status', 'n')
			])

		showdisks = self.str2bool(showdisks)
		showstatus = self.str2bool(showstatus)

		hosts = self.getHostnames(args)

		if showstatus:
			vm_status = self.getStatus(args, hosts)
		
		self.beginOutput()

		for host in hosts:
			vmnodeid = None
			mem = None
			cpus = None
			slice = None
			macs = None
			disks = None
			physhost = None

			if showstatus:
				status = None
				if vm_status.has_key(host):
					status = vm_status[host]

			#
			# get the physical node that houses this VM
			#
			rows = self.db.execute("""select vn.physnode from
				vm_nodes vn, nodes n where n.name = '%s'
				and n.id = vn.node""" % (host))

			if rows == 1:
				physnodeid, = self.db.fetchone()
			else:
				continue

			rows = self.db.execute("""select name from nodes where
				id = %s""" % (physnodeid))

			if rows == 1:
				physhost, = self.db.fetchone()
			else:
				continue

			#
			# get the VM configuration parameters
			#
			rows = self.db.execute("""select vn.id, vn.mem,
				n.cpus, vn.slice from nodes n, vm_nodes vn
				where vn.node = n.id and n.name = '%s'""" %
				host)

			if rows < 1:
				continue

			for vmnodeid, mem, cpus, slice in self.db.fetchall():
				if not vmnodeid:
					continue

				rows = self.db.execute("""select net.mac from
					networks net, nodes n, vm_nodes vn
					where vn.node = n.id and
					net.node = n.id and
					n.name = '%s'""" % host)

				if rows > 0:
					macs = self.db.fetchall()
					mac, = macs[0]
				else:
					macs = []
					mac = None

				disks = []
				rows = self.db.execute("""select vbd_type,
					prefix, name, device, mode, size from
					vm_disks where vm_node = %s""" %
					vmnodeid)
				if rows > 0:
					for vbd_type, prefix, name, device, \
						mode, size in \
						self.db.fetchall():

						file = os.path.join(prefix,
							name)

						disk = '%s:%s,%s,%s' % \
							(vbd_type, file,
							device, mode)
						disks.append((disk, size))

				if len(disks) > 0:
					(disk, disksize) = disks[0]

				info = (slice, mem, cpus, mac, physhost)
				if showstatus:
					info += (status,)
				if showdisks:
					info += (disk, disksize)

				self.addOutput(host, info)

				index = 1
				while len(macs) > index or len(disks) > index:
					if len(macs) > index:
						mac, = macs[index]
					else:
						mac = ''

					if len(disks) > index:
						disk, disksize = disks[index]
					else:
						disk = ''
						disksize = ''

					info = (None, None, None, mac, None)
					if showstatus:
						info += (None,)
					if showdisks:
						info += (disk, disksize)

					self.addOutput(host, info)

					index += 1

		header = [ 'vm-host', 'slice', 'mem', 'cpus', 'mac', 'host' ]
		if showstatus:
			header.append('status')
		if showdisks:
			header += [ 'disk', 'disksize' ]

		self.endOutput(header)

