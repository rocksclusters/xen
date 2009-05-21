# $Id: __init__.py,v 1.20 2009/05/21 21:14:43 bruno Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# Revision 1.20  2009/05/21 21:14:43  bruno
# tweaks
#
# Revision 1.19  2009/05/01 19:07:33  mjk
# chimi con queso
#
# Revision 1.18  2009/04/22 17:52:28  bruno
# allow the user to set the size of the frontend disk size.
#
# Revision 1.17  2009/03/30 19:15:46  bruno
# change first free VLAN id from 3 back to 2. this reverses a previous change.
# we found that the root cause of the problem was identical MAC addresses for
# the public side of virtual frontends. we not have a strategy to allocate
# unique MAC addresses for virtual clusters.
#
# Revision 1.16  2009/03/21 22:22:55  bruno
#  - lights-out install of VM frontends with new node_rolls table
#  - nuked 'site' columns and tables from database
#  - worked through some bugs regarding entities
#
# Revision 1.15  2009/02/12 05:15:35  bruno
# add and remove virtual clusters faster
#
# Revision 1.14  2009/02/09 00:29:04  bruno
# parallelize 'rocks sync host network'
#
# Revision 1.13  2009/01/14 00:20:55  bruno
# unify the physical node and VM node boot action functionality
#
# - all bootaction's are global
#
# - the node table has a 'runaction' (what bootaction should the node do when
#   a node normally boots) and an 'installaction (the bootaction for installs).
#
# - the 'boot' table has an entry for each node and it dictates what the node
#   will do on the next boot -- it will look up the runaction in the nodes table
#   (for a normal boot) or the installaction in the nodes table (for an install).
#
# Revision 1.12  2009/01/07 18:55:41  bruno
# change first free VLAN id from 2 to 3.
#
# it seems that there are often problems with VLAN 2 going up and down while
# VLAN 3 is solid.
#
# Revision 1.11  2008/12/16 00:45:04  bruno
# merge vm_profiles and pxeaction tables into bootaction table
#
# Revision 1.10  2008/10/31 19:56:55  bruno
# one more fix
#
# Revision 1.9  2008/10/27 19:25:01  bruno
# folded 'rocks * host vm boot' commands into 'rocks * host vm'
#
# Revision 1.8  2008/10/18 00:56:22  mjk
# copyright 5.1
#
# Revision 1.7  2008/09/22 20:21:28  bruno
# add 'vlan' to the list of parameters
#
# Revision 1.6  2008/09/04 20:06:06  bruno
# thanks phil!
#
# Revision 1.5  2008/09/04 19:54:37  bruno
# use 'rocks set vm boot' to install VM frontends
#
# Revision 1.4  2008/09/04 15:54:16  bruno
# xen tweaks
#
# Revision 1.3  2008/08/27 22:22:02  bruno
# add a 'Hosted VM' appliance
#
# Revision 1.2  2008/08/22 23:25:56  bruno
# closer
#
# Revision 1.1  2008/08/20 22:52:58  bruno
# install a virtual cluster of any size in 6 simple steps!
#
#
#

import os
import rocks.commands

class Command(rocks.commands.add.command):
	"""
	Add a VM-based cluster to an existing physical cluster.
	
	<arg type='string' name='fqdn' optional='0'>
	The FQDN for the virtual frontend.
	</arg>

	<arg type='string' name='ip' optional='0'>
	The IP address for the virtual frontend.
	</arg>

	<arg type='string' name='num-computes' optional='0'>
	The number of compute nodes VMs to associate with the frontend.
	</arg>

	<param type='string' name='fqdn'>
	Can be used in place of the fqdn argument.
	</param>

	<param type='string' name='ip'>
	Can be used in place of the ip argument.
	</param>

	<param type='string' name='num-computes'>
	Can be used in place of the num-computes argument.
	</param>

	<param type='string' name='cpus-per-compute'>
	The number of CPUs to allocate to each VM compute node. The default
	is 1.
	</param>

	<param type='string' name='disk-per-compute'>
	The size of the disk (in gigabytes) to allocate to each VM compute
	node. The default is 36.
	</param>

	<param type='string' name='disk-per-frontend'>
	The size of the disk (in gigabytes) to allocate to the VM frontend
	node. The default is 36.
	</param>

	<param type='string' name='mem-per-compute'>
	The amount of memory (in megabytes) to allocate to each VM compute
	node. The default is 1024.
	</param>

	<param type='string' name='vlan'>
	The VLAN ID to assign to this cluster. All network communication
	between the nodes of the virtual cluster will be encapsulated within
	this VLAN.
	The default is the next free VLAN ID.
	</param>

	<param type='string' name='container-hosts'>
	A list of VM container hosts that will be used to hold the VM
	compute nodes. This must be a space-separated list (e.g.,
	container-hosts="vm-container-0-0 vm-container-0-1").
	The default is to allocate the compute nodes in a round robin fashion
	across all the VM containers.
	</param>

	<example cmd='add cluster vm.cluster.org 1.2.3.4 2'>
	Create one frontend VM and assign it the name 'vm.cluster.org' with
	the IP address '1.2.3.4' and create 2 compute node VMs.
	</example>
	"""

	def getFreeVlan(self):
		#
		# make a list of the used vlan ids
		#
		self.db.execute("""select distinctrow vlanid from networks
			order by vlanid""")

		vlanids = []
		for v, in self.db.fetchall():
			if v:
				vlanids.append(v)

		#
		# find a free vlanid
		#
		for i in range(2, 4096):
			if i not in vlanids:
				return i

		return None


	def getVMContainers(self):
		containers = []

		#
		# now get all the VM containers
		#
		self.db.execute("""select n.name from nodes n, memberships m
			where n.membership = m.id and
			m.name = 'VM Container' """)
			
		for container, in self.db.fetchall():
			containers.append(container)

		return containers


	def getFrontend(self):
		fqdn = os.uname()[1]
		return fqdn.split('.')[0]


	def configVlan(self, vlan):
		hosts = []

		#
		# create a list of all the physical machines that can host
		# VMs. we'll assume the local machine can host VMs.
		#
		hosts.append(self.getFrontend())
		hosts += self.getVMContainers()

		#
		# configure the vlan for each host
		#
		for host in hosts:
			#
			# add the vlan definition to the database
			#
			self.command('add.host.interface', [ host,
				'iface=vlan%d' % vlan, 'subnet=private',
				'vlan=%d' % vlan])

		#
		# reconfigure the network stack on the host
		#
		# need to catch exceptions -- when the network is
		# reconfigured on a remote host, the connection is
		# dropped, which results in an I/O error
		#
		try:
			self.command('sync.host.network', hosts)
		except:
			pass


	def createFrontend(self, vlan, fqdn, ip, disksize, gateway):
		output = self.command('add.host.vm', [ self.getFrontend(),
			'membership=Frontend', 'num-macs=2',
			'disksize=%s' % disksize, 'vlan=%d,0' % vlan,
			'sync-config=n' ] )

		self.frontendname = None

		line = output.split()
		if line[0] == 'added' and line[1] == 'VM':
			self.frontendname = line[2]
		else:
			self.abort('failed to create a frontend VM on host %s'
				% self.getFrontend())

		#
		# configure the public network for the VM frontend
		#
		self.command('set.host.interface.subnet', [ self.frontendname,
			'eth1', 'public' ] )
		self.command('set.host.interface.ip', [ self.frontendname,
			'eth1', ip ] )
		self.command('set.host.interface.name', [ self.frontendname,
			'eth1', fqdn ] )
		if not gateway:
			gateway = self.db.getHostAttr(self.frontendname,
				'Kickstart_PublicGateway')
		self.command('add.host.route', [ self.frontendname, '0.0.0.0',
			gateway, 'netmask=0.0.0.0' ] )

		#
		# set the run and install actions for this VM
		#
		self.command('set.host.runaction', [ self.frontendname,
			'none' ] )
		self.command('set.host.installaction', [ self.frontendname,
			'install vm frontend' ] )

		#
		# set the default boot action to be 'install'
		#
		self.command('set.host.boot', [ self.frontendname,
			'action=install' ] )

		self.addOutput('', 'created frontend VM named: %s' % 
			self.frontendname)


	def createComputes(self, vlan, computes, containers,
		cpus_per_compute, mem_per_compute, disk_per_compute):

		self.computenames = []

		for i in range(0, computes):
			host = containers[i % len(containers)]

			output = self.command('add.host.vm', [ host,
				'membership=Hosted VM', 'num-macs=1',
				'cpus=%s' % cpus_per_compute,
				'mem=%s' % mem_per_compute,
				'disksize=%s' % disk_per_compute,
				'vlan=%d' % vlan,
				'sync-config=n' ] )

			line = output.split()
			if line[0] == 'added' and line[1] == 'VM':
				self.computenames.append(line[2])
			else:
				self.abort('failed to create a compute VM ' + 
					'on host %s' % host)

			
			#
			# set the run and install actions for this VM
			#
			self.command('set.host.runaction', [ line[2], 
				'none' ] )
			self.command('set.host.installaction', [ line[2], 
				'install vm' ] )

			#
			# set the default boot action to be 'install'
			#
			self.command('set.host.boot', [ line[2], 
				'action=install' ] )

			self.addOutput('', '\tcreated compute VM named: %s' % 
				line[2])


	def run(self, params, args):
		self.beginOutput()

		(args, fqdn, ip, num_computes) = self.fillPositionalArgs(
			('fqdn', 'ip', 'num-computes'))

		if not fqdn:
			self.abort('must supply an FQDN for the frontend')
		if not ip:
			self.abort('must supply an IP address for the frontend')
		if not num_computes:
			self.abort('must supply the number of compute nodes')

		try:
			computes = int(num_computes)
		except:
			self.abort('num-computes must be an integer')

		#
		# fillParams with the above default values
		#
		(cpus_per_compute, mem_per_compute, disk_per_compute,
			disk_per_frontend, container_hosts, vlan, gateway) = \
			self.fillParams(
				[('cpus-per-compute', 1),
				('mem-per-compute', 1024),
				('disk-per-compute', 36),
				('disk-per-frontend', 36),
				('container-hosts', None),
				('vlan', None),
				('gateway', None)
				])

		if vlan:
			try:
				vlanid = int(vlan)
			except:
				self.abort('Vlan ID (%s) must be an integer'
					% vlan)
		else:
			vlanid = self.getFreeVlan()

			if not vlanid:
				self.abort('could not find a free Vlan ID')

		if container_hosts:
			containers = container_hosts.split()
		else:
			containers = self.getVMContainers()

		#
		# configure the vlan on each physical node that can hold
		# a VM
		#
		self.configVlan(vlanid)

		#
		# create the frontend VM
		#
		self.createFrontend(vlanid, fqdn, ip, disk_per_frontend,
			gateway)

		#
		# create the compute nodes
		#
		self.createComputes(vlanid, computes, containers,
			cpus_per_compute, mem_per_compute, disk_per_compute)

		#
		# reconfigure and restart the appropriate rocks services
		#
		self.command('sync.config')

		self.endOutput()

