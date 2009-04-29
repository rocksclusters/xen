# $Id: __init__.py,v 1.5 2009/04/29 17:37:38 bruno Exp $
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
# Revision 1.5  2009/04/29 17:37:38  bruno
# make sure libvirt is properly imported
#
# Revision 1.4  2009/04/08 22:27:58  bruno
# retool the xen commands to use libvirt
#
# Revision 1.3  2008/10/18 00:56:24  mjk
# copyright 5.1
#
# Revision 1.2  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.1  2008/02/07 20:08:24  bruno
# retooled the commands and database tables to handle moving running VMs
#
#

import os
import rocks.commands
import rocks.vm

import sys
sys.path.append('/usr/lib64/python2.4/site-packages')
sys.path.append('/usr/lib/python2.4/site-packages')
import libvirt

class Command(rocks.commands.restore.host.command):
	"""
	Restore a VM on a physical node. This command restores a previously
	saved VM.

	<arg type='string' name='host' repeat='1'>
	A list of one or more VM host names.
	</arg>

	<arg type='string' name='file'>
	The file name the saved VM state is stored in. If you don't
	supply this parameter, then the default file name is:
	/&lt;largest-partition-on-physical-host&gt;/xen/disks/&lt;vm-name%gt;.saved.
	For example, on a physical node with the default partitioning, the
	file that contains the state for VM compute-0-0-0 is:
	/state/partition1/xen/disks/compute-0-0-0.saved
	</arg>

	<example cmd='restore host vm compute-0-0-0'>
	Restore VM host compute-0-0-0.
	</example>
	"""

	def run(self, params, args):
		file, = self.fillParams( [('file', None)] )
		hosts = self.getHostnames(args)

		if len(hosts) < 1:
			self.abort('must supply host')

		if file and len(hosts) > 1:
			self.abort('if you supply the "file" parameter, ' +
				'then you only can specify one VM host')

		vm = rocks.vm.VM(self.db)

		for host in hosts:
			physhost = vm.getPhysHost(host)

			if not file:
				diskprefix = vm.getLargestPartition(physhost)
				if diskprefix:
					file = os.path.join(diskprefix,
						'xen/disks/%s.saved' % host)

			if physhost and file:
				#
				# send the restore command to the physical node
				#
				hipervisor = libvirt.open('xen://%s/'
					% physhost)
				domU = hipervisor.lookupByName(host)
				domU.restore(file)

