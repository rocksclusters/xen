# $Id: __init__.py,v 1.2 2008/09/25 17:56:54 bruno Exp $
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
# Revision 1.2  2008/09/25 17:56:54  bruno
# can't have spaces after the 'related' tag. otherwise, the xen usersguide
# will not build
#
# Revision 1.1  2008/09/02 23:30:43  phil
# Add set method for modifying bootprofiles
#

import sys
import string
import rocks.commands
import os

class Command(rocks.commands.HostArgumentProcessor, rocks.commands.set.host.command):
	"""
	Add a boot profile for virtual a host.
	
	<arg type='string' name='host' repeat='1' optional='1'>
	List of hosts to add profile definitions. If no hosts are listed,
	then the global definition for 'profile=name' is added.
	</arg>

	<param type='string' name='profile'>
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
	
	<example cmd='set host vm bootprofile profile=install kernel="file:///boot/kickstart/xen/vmlinuz-experimental"'>
	Change the kernel to vmlinuz-experimental for the global install profile 
	</example>

	<related>set host vm boot</related>
	<related>list host vm boot</related>
	<related>list host vm bootprofile</related>
	<related>add host vm bootprofile</related>
	<related>remove host vm bootprofile</related>
	"""

	def run(self, params, args):
		callArgs = []
		if (args):
			callArgs.append(args)

		for key in params.keys():
			callArgs.append("%s=%s" % (key,params[key]))

		self.command('add.host.vm.bootprofile',callArgs)
