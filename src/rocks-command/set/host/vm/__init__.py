# $Id: __init__.py,v 1.3 2008/10/18 00:56:24 mjk Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		           version 5.1  (VI)
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
# Revision 1.3  2008/10/18 00:56:24  mjk
# copyright 5.1
#
# Revision 1.2  2008/04/21 16:37:35  bruno
# nuked the vm_macs table -- now using the networks table to store/retrieve
# mac addresses for VMs
#
# Revision 1.1  2008/04/17 23:23:39  bruno
# you now can change the number of cpus and memory allocated to VMs.
#
#
#

import os.path
import rocks.commands


class Command(rocks.commands.HostArgumentProcessor, rocks.commands.set.command):
	"""
	Change the VM configuration for a specific VM.
	
	<arg type='string' name='host' optional='0'>
	One or more VM host names.
	</arg>

	<param type='string' name='physnode'>
	The physical machine this VM should run on.
	</param>

	<param type='string' name='disk'>
	A VM disk specification. More than one disk can be supplied. Each
	disk specification must separated by a space.
	</param>

	<param type='string' name='disksize'>
	The size of the VM disk. 
	</param>

	<param type='string' name='mem'>
	The amount of memory in megabytes to assign to this VM.
	</param>

	<param type='string' name='slice'>
	The slice ID for this VM.
	</param>

	<param type='string' name='virt-type'>
	Set the virtualization type for this VM. This can be 'para' or
	'hardware'.
	</param>

	<example cmd='set host vm compute-0-0-0 mem=4096'>
	Change the memory allocation for VM compute-0-0-0 to 4 GB.
	</example>
	"""

	def addDiskSpec(self, vmnodeid, disk, disksize):
		#
		# parse the disk specification
		#
		d = disk.split(',')
		if len(d) != 3:
			self.abort('invalid disk specification: "%s"' % disk)

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

	def run(self, params, args):
		mem = None

		(physnode, disk, disksize, m, slice, virt_type) = \
			self.fillParams([ ('physnode', None), ('disk', None),
				('disksize', None), ('mem', None),
				('slice', None), ('virt-type', None) ])

		try:
			if m:
				mem = int(m)
		except:
			self.abort('"mem" parameter must be an integer')

		if physnode:
			p = self.getHostnames([physnode])
			if len(p) == 0:
				self.abort('physnode "%s" does not exist'
					% (physnode))
			if len(p) > 1:
				self.abort('too many physnodes. ' +
					'only supply one physnode')
		
		hosts = self.getHostnames(args)

		if len(hosts) != 1:
			self.abort('must supply only one host')

		host = hosts[0]

		rows = self.db.execute("""select vn.id from nodes n,
			vm_nodes vn where vn.node = n.id and
			n.name = '%s'""" % host)

		if rows == 0:
			#
			# there is no VM specification in the database.
			# let's create a basic row for this VM
			#
			rows = self.db.execute("""select id from nodes where
				name = '%s'""" % host)

			#
			# we know that 'host' is in the nodes table, otherwise
			# getHostnames above would have returned a zero-length
			# list
			#
			vmnode, = self.db.fetchone()

			rows = self.db.execute("""insert into vm_nodes
				(node) values ('%d')""" % (vmnode))

			if rows == 1:
				rows = self.db.execute("""select
					last_insert_id()""")
				if rows == 1:
					vmnodeid, = self.db.fetchone()
				else:
					self.abort('could not get node id ' +
						'for new VM')
		else:
			vmnodeid, = self.db.fetchone()

		if physnode:
			rows = self.db.execute("""select id from nodes where
				name = '%s'""" % (physnode))
		
			physnodeid, = self.db.fetchone()

			self.db.execute("""update vm_nodes set
				physnode = '%s' where id = '%s'""" %
				(physnodeid, vmnodeid))
			
		if disk:
			#
			# first remove all disk entries
			#
			self.db.execute("""delete from vm_disks where
				vm_node = %s""" % vmnodeid)

			#
			# then add them back
			#
			index = 0
			if disksize:
				ds = disksize.split(' ')
			else:
				ds = []

			for d in disk.split(' '):
				if len(ds) < index:
					dsize = '36'
				else:
					dsize = ds[index]

				self.addDiskSpec(vmnodeid, d, dsize)

				index += 1
				
		if mem:
			rows = self.db.execute("""update vm_nodes set
				mem = %d where id = %d""" %
				(mem, vmnodeid))

		if slice:
			rows = self.db.execute("""update vm_nodes set
				slice = %s where id = %d""" %
				(slice, vmnodeid))

		if virt_type and virt_type != 'None':
			rows = self.db.execute("""update vm_nodes set
				virt_type = %s where id = %d""" %
				(virt_type, vmnodeid))

