# $Id: __init__.py,v 1.8 2008/09/01 15:58:57 phil Exp $
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
# Revision 1.8  2008/09/01 15:58:57  phil
# Support start host vm install=y to force the node to boot its install profile.
# Requires rocks-pygrub to be the bootloader.
#
# Revision 1.7  2008/07/01 22:57:09  bruno
# fixes to the xen reports which generate xen configuration files
#
# Revision 1.6  2008/04/17 16:38:21  bruno
# incorporate phil's vm changes
#
# Revision 1.5  2008/03/06 23:42:05  mjk
# copyright storm on
#
# Revision 1.4  2008/02/08 23:29:59  bruno
# tune
#
# Revision 1.3  2008/02/02 00:01:58  bruno
# fixes
#
# Revision 1.2  2008/02/01 21:38:54  bruno
# closer
#
# Revision 1.1  2008/01/29 00:20:08  bruno
# split 'rocks boot' into 'rocks create' and 'rocks start'
#
#

import os
import tempfile
import rocks.commands

class Command(rocks.commands.start.host.command):
	"""
	Boots a VM slice on a physical node.

	<arg type='string' name='host' repeat='1'>
	A list of one or more VM host names.
	</arg>

        <param name='install' type='bool' optional='1'>
        If install='y' is set, then the VM will be first boot from
        its install bootprofile. Default is 'n'

        VMs use different mechanisms to control booting as compared to
        PXE-booted hosts. However, If the pxeaction for a VM host is
        defined explicitly as "install*' for this VM, then
        this flag will be internally set to 'y'.

        </param>

	<example cmd='start host vm compute-0-0-0'>
	Start VM host compute-0-0-0.
	</example>

	<example cmd='start host vm install=y compute-0-0-0'>
	Start VM host compute-0-0-0 in installation mode.
	</example>

	<related> set host vm boot </related>
	<related> list host vm bootprofile </related>
	<related> add host vm bootprofile </related>
	<related> remove host vm bootprofile </related>
	<related> set host vm bootprofile </related>
	"""

	def run(self, params, args):
		hosts = self.getHostnames(args)
		
		if len(hosts) < 1:
			self.abort('must supply at least one host')

                (forceInstall, ) = self.fillParams([('install','n')])

		for host in hosts:
			#
			# the name of the physical host that will boot
			# this VM host
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
			# create the configuration file
			#
			temp = tempfile.mktemp()
			fout = open(temp, 'w')
			fout.write(self.command('report.host.vm', [host,
				'install=%s' % forceInstall ]))
			fout.close()
			os.system('scp -q %s %s:/etc/xen/rocks/%s' % 
				(temp, physhost, host))
			os.unlink(temp)

			os.system('ssh -q %s "xm create /etc/xen/rocks/%s"' % 
				(physhost, host))
		
