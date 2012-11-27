# $Id: __init__.py,v 1.4 2012/11/27 00:49:40 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.6 (Emerald Boa)
# 		         version 6.1 (Emerald Boa)
# 
# Copyright (c) 2000 - 2013 The Regents of the University of California.
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
# Revision 1.4  2012/11/27 00:49:40  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.3  2012/05/06 05:49:51  phil
# Copyright Storm for Mamba
#
# Revision 1.2  2011/07/23 02:31:44  phil
# Viper Copyright
#
# Revision 1.1  2011/01/12 21:01:12  bruno
# added a report to create the xendomains configuration file
#
# nuked vm-container.xml and vm-container-client.xml. we don't need these
# since xen-enabled nodes are now configured with the xen attribute.
#
#

import rocks.commands
import rocks.vm

class Command(rocks.commands.report.host.command):
	"""
	Generates the /etc/sysconfig/xendomains configuration file for a
	host.
	
	<example cmd="report host xen xendomains vm-container-0-0">
	</example>
	"""
		
	def run(self, params, args):
		vars = [ ('XENDOMAINS_SYSRQ', '""'),
			('XENDOMAINS_USLEEP', '100000'),
			('XENDOMAINS_CREATE_USLEEP', '5000000'),
			('XENDOMAINS_MIGRATE', '""'),
			('XENDOMAINS_SHUTDOWN', '"--halt --wait"'),
			('XENDOMAINS_SHUTDOWN_ALL', '"--all --halt --wait"'),
			('XENDOMAINS_RESTORE', 'true'),
			('XENDOMAINS_AUTO_ONLY', 'false'),
			('XENDOMAINS_STOP_MAXWAIT', '300') ]

		vm = rocks.vm.VM(self.db)

		hosts = self.getHostnames(args)
		if len(hosts) != 1:
			self.abort('must only supply one host')

		self.addText('<file name="/etc/sysconfig/xendomains">')

		host = hosts[0]
		for var, default in vars:
			attr = self.db.getHostAttr(host, var)
			if not attr:
				attr = default
			self.addText('%s=%s\n' % (var, attr))

		#
		# special case for XENDOMAINS_SAVE and XENDOMAINS_AUTO.
		# if an attribute is not set for these variables, then
		# we want to put them on the largest partition on the
		# host
		#
		part = vm.getLargestPartition(host)

		attr = self.db.getHostAttr(host, 'XENDOMAINS_SAVE')
		if not attr:
			attr = '%s/xen/save' % part
		self.addText('XENDOMAINS_SAVE=%s\n' % (attr))
		xendomains_save = attr

		attr = self.db.getHostAttr(host, 'XENDOMAINS_AUTO')
		if not attr:
			attr = '%s/xen/auto' % part
		self.addText('XENDOMAINS_AUTO=%s\n' % (attr))
		xendomains_auto = attr

		self.addText('</file>\n\n')

		self.addText('mkdir -p %s\n' % xendomains_save)
		self.addText('mkdir -p %s\n' % xendomains_auto)

