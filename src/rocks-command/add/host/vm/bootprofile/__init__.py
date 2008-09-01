# $Id: __init__.py,v 1.1 2008/09/01 03:35:35 phil Exp $
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
# $Log

import sys
import string
import rocks.commands
import os

class Command(rocks.commands.HostArgumentProcessor,
	rocks.commands.add.command):
	"""
	Add a boot profile for virtual a host.
	
	<arg type='string' name='host' repeat='1' optional='1'>
	List of hosts to add profile definitions. If no hosts are listed,
	then the global definition for 'profile=name' is added.
	</arg>

	<param type='string' name='action'>
	Label name for the boot profile. You can see the profile
	label names by executing: 'rocks list host vm bootprofile [host(s)]'.
	</param>
	
	<param type='string' name='kernel'>
	URL for the kernel associated with this profile
	(e.g., 'file:///boot/kickstart/xen/vmlinuz')
	</param>
	
	<param type='string' name='ramdisk'>
	URL for the kernel associated with this profile
	(e.g., 'file:///boot/kickstart/xen/initrd-xen.iso.gz')
	</param>
	
	<param type='string' name='args'>
	The second line for a pxelinux definition (e.g., append ks
	initrd=initrd.img ramdisk_size=150000 lang= devfs=nomount pxe
	kssendmac selinux=0)
	</param>
	
	<example cmd='add host vm bootprofile profile=install kernel="file:///boot/kickstart/xen/vmlinuz"'>
	Add the global 'install' boot profile 
	</example>
	
	<example cmd='add host vm bootprofile compute-0-0-0 profile=install kernel="http://10.1.1.1/xenkernels/experimental-vmlinuz"'>
	Add the 'install' profile for compute-0-0-0
	</example>
	"""

	def addProfile(self, nodeid, host, profile, kernel, ramdisk, bootargs):
		#
		# is there already an entry in the pxeaction table
		#
		rows = self.db.execute("""select id from vm_profiles where
			vm_node=%d and profile='%s'""" % (nodeid, profile))
		if rows < 1:
			#
			# insert a new row
			#
			cols = {}
			cols['vm_node'] = '%s' %  (nodeid)
			cols['profile'] = '"%s"' % (profile)

			if kernel != None:
				cols['kernel'] = '"%s"' % (kernel)
			if ramdisk != None:
				cols['ramdisk'] = '"%s"' % (ramdisk)
			if bootargs != None:
				cols['args'] = '"%s"' % (bootargs)

			self.db.execute('insert into vm_profiles '
				'(%s) ' % (string.join(cols.keys(), ',')) + \
				'values '
				'(%s) ' % (string.join(cols.values(), ',')))
		else:
			#
			# update the existing row
			#
			profileid, = self.db.fetchone()

			query = 'update vm_profiles set profile = "%s" ' % (profile)
			if kernel != None:
				query += ', kernel = "%s" ' % (kernel) 
			if ramdisk != None:
				query += ', ramdisk = "%s" ' % (ramdisk) 
			if bootargs != None:
				query += ', args = "%s" ' % (bootargs)

			query += 'where id = %s' % (profileid)

			self.db.execute(query)

		return


	def run(self, params, args):
		if len(args) == 0:
			hosts = []
		else:
			hosts = self.getHostnames(args)

		(profile, kernel, ramdisk, bootargs) = self.fillParams(
			[('profile', ), 
			('kernel', ), 
			('ramdisk', ),
			('args', )])
			
		if not profile:
			self.abort('must supply an profile name')

		if not hosts:
			#
			# set the global (all nodes) configuration
			#
			self.addProfile(0, 'global', profile, kernel, ramdisk,
				bootargs)

		else:
			for host in hosts:
				#
				# get the node from the nodes table
				#
				self.db.execute("""select v.id 
					from vm_nodes v, nodes n where
					n.name='%s' and v.node=n.id""" % (host))
				hostid, = self.db.fetchone()

				self.addProfile(hostid, host, profile,
					kernel, ramdisk, bootargs)
					
