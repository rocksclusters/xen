# $Id: __init__.py,v 1.16 2008/04/21 16:37:35 bruno Exp $
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
# Revision 1.16  2008/04/21 16:37:35  bruno
# nuked the vm_macs table -- now using the networks table to store/retrieve
# mac addresses for VMs
#
# Revision 1.15  2008/04/17 16:38:21  bruno
# incorporate phil's vm changes
#
# Revision 1.14  2008/04/15 20:29:16  bruno
# 'name' parameter now works
#
# Revision 1.13  2008/04/15 20:02:35  bruno
# now can use 'num-macs' parameter
#
# Revision 1.12  2008/03/12 19:30:08  bruno
# change default virtual block device (vbd) from tap:aio to file (file is
# more stable)
#
# Revision 1.11  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.10  2008/02/12 00:01:25  bruno
# fixes
#
# Revision 1.9  2008/02/08 23:29:59  bruno
# tune
#
# Revision 1.8  2008/02/07 20:08:24  bruno
# retooled the commands and database tables to handle moving running VMs
#
# Revision 1.7  2008/02/02 00:27:24  bruno
# can create multiple VMs with one command
#
# Revision 1.6  2008/02/01 21:38:54  bruno
# closer
#
# Revision 1.5  2008/01/30 22:01:34  bruno
# closer
#
# Revision 1.4  2008/01/30 01:46:58  bruno
# remove hardcode of '/state/partition1' for location of xen configuration
# files.
#
# if no disk specification is set, select the largest partition.
#
# Revision 1.3  2008/01/24 22:28:18  bruno
# change default file spec to 'tap:aio'
#
# Revision 1.2  2007/12/10 20:59:25  bruno
# fixes to get a VMs configured and running on newly installed xen-based
# physical machines.
#
# Revision 1.1  2007/12/03 19:48:51  bruno
# xen for V
#
#

import sys
import string
import os
import os.path
import IPy
import rocks.commands
import rocks.vm


class Command(rocks.commands.HostArgumentProcessor, rocks.commands.add.command):
	"""
	Add a VM specification to the database.
	
	<arg type='string' name='host' optional='0' repeat='1'>
	One or more physical host names.
	</arg>

	<arg type='string' name='membership' optional='0'>
	The membership to assign to the VM.
	</arg>

	<param type='string' name='membership'>
	Can be used in place of the membership argument.
	</param>

	<param type='string' name='name'>
	The name to assign to the VM (e.g., 'compute-0-0-0').
	</param>

	<param type='string' name='ip'>
	The IP address to assign to the VM.
	If no IP address is provided, then one will be automatically assigned.
	</param>

	<param type='string' name='subnet'>
	The subnet to associate to this VM.
	The default is: private.
	</param>

	<param type='string' name='mem'>
	The amount of memory in megabytes to assign to this VM.
	The default is: 1024.
	</param>

	<param type='string' name='cpus'>
	The number of CPUs to assign to this VM.
	The default is: 1.
	</param>

	<param type='string' name='slice'>
	The 'slice' id on the physical node. Each VM on a physical node has
	a unique slice number
	The default is the next available free slice number.
	</param>

	<param type='string' name='mac'>
	A MAC address to assign to this VM.
	If no MAC address is specified, the next free MAC address will be
	selected.
	</param>

	<param type='string' name='num-macs'>
	The number of MAC addresses to automatically assign to this VM.
	The default is 1.
	</param>
	
	<param type='string' name='disk'>
	A disk specification for this VM.
	The default is: file:/&lt;largest-partition-on-physical-node&gt;/xen/disks/&lt;vm-name&gt;.hda,hda,w
	</param>

	<param type='string' name='disksize'>
	The amount of disk space in gigabytes to assign to the disk
	specification.
	The default is: 36.
	</param>
	
	<example cmd='add host vm'>
	Create a default VM.
	</example>

	<example cmd='add host vm mem=4096'>
	Create a VM and allocate 4 GB of memory to it.
	</example>
	"""

	def addToDB(self, nodename, membership, ip, subnet, physnodeid, rack,
		rank, mem, cpus, slice, mac, num_macs, disk, disksize):

		#
		# need to add entry in node and networks tables here
		#
		rows = self.db.execute("""select id from memberships where
			name = '%s'""" % (membership))

		if rows == 1:
			membershipid, = self.db.fetchone()
		else:
			self.abort('could not get membership id for ' + 
				'membership "%s"' % (membership))

		rows = self.db.execute("""select id from subnets where
			name = '%s'""" % (subnet))

		if rows == 1:
			subnetid, = self.db.fetchone()
		else:
			self.abort('could not get subnet id for ' + 
				'subnet "%s"' % (subnet))

		#
		# check if the nodename is already in the nodes table. if
		# so, abort.
		#
		rows = self.db.execute("""select id from nodes where
			name = '%s'""" % (nodename))

		if rows > 0:
			self.abort('node "%s" is ' % (nodename) + \
				'already in the database')

		#
		# we're good to go -- add the VM to the nodes table
		#
		rows = self.db.execute("""insert into nodes (name, membership,
			cpus, rack, rank) values ('%s', %s, %s, %s, %s)""" %
			(nodename, membershipid, cpus, rack, rank))

		if rows == 1:
			rows = self.db.execute("""select last_insert_id()""")
			if rows == 1:
				vmnodeid, = self.db.fetchone()
			else:
				self.abort('could not get node id for new VM')

		self.db.execute("""insert into networks (node, mac, ip, name,
			device, subnet, module) values (%s, '%s', '%s', '%s',
			'%s', %s, '%s')""" % (vmnodeid, mac, ip, nodename,
			'eth0', subnetid, 'xennet'))

		#
		# put in additional MACs here
		#
		for m in range(1, num_macs):
			mac = self.getNextMac()

			self.db.execute("""insert into networks (node, mac,
				device, module) values (%s, '%s', '%s', '%s')
				""" % (vmnodeid, mac, 'eth%d' % (m) , 'xennet'))

		rows = self.db.execute("""insert into vm_nodes (physnode, node,
			mem, slice) values (%s, %s, %s, %s)""" %
			(physnodeid, vmnodeid, mem, slice))

		if rows == 1:
			rows = self.db.execute("""select last_insert_id()""")
			if rows == 1:
				vmnodeid, = self.db.fetchone()

		if rows != 1:
			#
			# an error occurred, don't continue
			#
			self.abort('could not update the vm_nodes table')

		#
		# parse the disk specification
		#
		d = disk.split(',')
		if len(d) != 3:
			self.abort('invalid disk specification')

		device = d[1]
		mode = d[2]

		e = d[0].split(':')
		vbd_type = ':'.join(e[0:-1])
		prefix = os.path.dirname(e[-1])
		name = os.path.basename(e[-1])

		self.db.execute("""insert into vm_disks (vm_node, vbd_type,
			prefix, name, device, mode, size)
			values (%s, '%s', '%s', '%s', '%s', '%s', %s)""" %
			(vmnodeid, vbd_type, prefix, name, device, mode,
			disksize))


	def getNodename(self, membership, rack, rank, slice):
		nodename = None

		#
		# get the appliance basename for this membership
		#
		rows = self.db.execute("""select a.name from appliances a,
			memberships m where m.name = '%s' and
			m.appliance = a.id""" % (membership))

		if rows == 1:
			basename, = self.db.fetchone()
			nodename = '%s-%s-%s-%s' % (basename, rack, rank, slice)

		return nodename


	def getNextIP(self, name):
		rows = self.db.execute("""select subnet, netmask from subnets
			where name = '%s'""" % (name))

		if rows != 1:
			return None

		subnet, netmask = self.db.fetchone()

		ipinfo = IPy.IP('%s/%s' % (subnet, netmask))

		bcast = ipinfo.broadcast()
		net = ipinfo.net()

		firstip = '%s' % IPy.IP(net.int() + 1)

		rows = self.db.execute("""select ip from networks""")

		knownips = []
		if rows > 0:
			knownips = self.db.fetchall()

		index = 1
		ip = None
		while 1:
			lastip = '%s' % IPy.IP(bcast.int() - index)

			if lastip == firstip:
				break

			if (lastip,) not in knownips:
				ip = lastip
				break

			index += 1

		return ip


	def getNextMac(self):
		#
		# find the next free MAC address in the database
		#
		rows = self.db.execute("""select mac from networks where mac
			like '00:16:3e:%'""")

		max = 0
		if rows > 0:
			for mac, in self.db.fetchall():
				m = string.split(mac, ':')
				x = int(m[3], 16) * (2 ** 16)
				x += int(m[4], 16) * (2 ** 8)
				x += int(m[5], 16)
	
				if x > max:
					max = x

		max += 1

		mac = '00:16:3e'
		mac += ':%02x' % ((max & 0xff0000) >> 16)
		mac += ':%02x' % ((max & 0xff00) >> 8)
		mac += ':%02x' % (max & 0xff)

		return mac


	def addVMHost(self, host, membership, nodename, ip, subnet, mem, cpus,
		slice, mac, num_macs, disk, disksize):

		rows = self.db.execute("""select id, rack, rank from nodes where
			name = '%s'""" % (host))

		if rows == 1:
			nodeid, rack, rank = self.db.fetchone()
		else:
			self.abort('could not find an ID for host %s' % (host))

		rows = self.db.execute("""select name from nodes""")
		knownhosts = self.db.fetchall()

		if not slice:
			#
			# find the next free slice in the database
			#
			rows = self.db.execute("""select max(slice) from
				vm_nodes where physnode = %s""" % (nodeid))

			if rows > 0:
				max, = self.db.fetchone()
				if max:
					slice = int(max) + 1
				else:
					slice = 0

			#
			# special case where the user didn't specify the
			# slice *and* the nodename, then we are allowed to
			# increment the slice value until we find a unique
			# nodename
			#
			while not nodename:
				nodename = self.getNodename(membership, rack,
					rank, slice)

				if (nodename,) in knownhosts:
					nodename = None
					slice += 1

		if not nodename:
			nodename = self.getNodename(membership, rack, rank,
				slice)

			if (nodename,) in knownhosts:
				#
				# make sure the nodename is not already in
				# the database
				#
				self.abort('nodename (%s) ' % nodename + \
					'is already in the databaase')
			
		if not disk:
			#
			# find the largest partition on the remote node
			# and use it as the directory prefix
			#
			vm = rocks.vm.VM(self.db)

			vbd_type = 'file'
			prefix = vm.getLargestPartition(host)
			device = 'hda'
			name = '%s.%s' % (nodename, device)
			mode = 'w'

			if not prefix:
				self.abort('could not find a partition on '
					+ 'host (%s) to hold the ' % host
					+ 'VM\'s disk image')

			disk = '%s:%s,%s,%s' % (vbd_type, 
				os.path.join(prefix, 'xen/disks', name),
				device, mode)

		if not mac:
			mac = self.getNextMac()

		if not ip:
			ip = self.getNextIP(subnet)

		#
		# we now have all the parameters -- add them to the database
		#
		self.addToDB(nodename, membership, ip, subnet, nodeid, rack,
			rank, mem, cpus, slice, mac, num_macs, disk, disksize)

		#
		# print the name of the new VM
		#
		self.beginOutput()
		self.addOutput('',
			'added VM on node "%s" slice "%s" with vm_name "%s"'
			% (host, slice, nodename))
		self.endOutput()


	def run(self, params, args):
		(args, membership) = self.fillPositionalArgs(('membership', ))

		if not membership:
			self.abort('must supply a membership')

		if not len(args):
			self.abort('must supply at least one host')

		#
		# fillParams with the above default values
		#
		(nodename, ip, subnet, mem, cpus, slice, mac, macs, disk,
			disksize) = self.fillParams(
				[('name', None),
				('ip', None),
				('subnet', 'private'),
				('mem', 1024),
				('cpus', 1),
				('slice', None),
				('mac', None),
				('num-macs', '1'),
				('disk', None),
				('disksize', 36)])

		hosts = self.getHostnames(args)

		if len(hosts) > 1:
			if nodename:
				self.abort("can't supply the 'name' " +
					"parameter with more than one host")
			if ip:
				self.abort("can't supply the 'ip' " +
					"parameter with more than one host")
			if slice:
				self.abort("can't supply the 'slice' " +
					"parameter with more than one host")
			if mac:
				self.abort("can't supply the 'mac' " +
					"parameter with more than one host")

		try:
			num_macs = int(macs)
		except:
			self.abort("the num_macs parameter must be an integer")
			
		for host in hosts:
			self.addVMHost(host, membership, nodename, ip, subnet,
				mem, cpus, slice, mac, num_macs, disk, disksize)
		
		#
		# reconfigure and restart the appropriate rocks services
		#
		self.command('sync.config')

