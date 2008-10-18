# $Id: __init__.py,v 1.3 2008/10/18 00:56:23 mjk Exp $
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
# Revision 1.3  2008/10/18 00:56:23  mjk
# copyright 5.1
#
# Revision 1.2  2008/09/25 17:56:54  bruno
# can't have spaces after the 'related' tag. otherwise, the xen usersguide
# will not build
#
# Revision 1.1  2008/09/01 14:30:29  phil
# List the active run and install profile. Add related to docstring
#
#

import sys
import socket
import rocks.commands
import string

class Command(rocks.commands.list.host.command):
	"""
	Lists the names of the install and run bootprofiles for [host(s)] . 
	
	The a named profile describes the combination of kernel, ramdisk
        args that would be used if that profile where referenced for by the 
	The RunProfile references the combination when a VM is booted for
	running (usually this is None). The InstallProfile references the 
	combination when the nodes is booted in install mode. 
	
	When the RunProfile is None, the VM node will 
	boot from the kernel defined in its image. 

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, info about
	all the known hosts is listed.
	</arg>

	<example cmd='list host vm boot compute-0-0-0'>
	List the active run and install profiles defined for compute-0-0-0.
	</example>

	<example cmd='list host vm boot'>
	List the active run and install profiles defined all known VM hosts.
	</example>

	<related>set host vm boot</related>
	<related>list host vm bootprofile</related>
	<related>add host vm bootprofile</related>
	<related>remove host vm bootprofile</related>
	<related>set host vm bootprofile</related>
	"""

	def run(self, params, args):

		self.beginOutput()

		for host in self.getHostnames(args):
			# get profiles defined just for the node
			self.db.execute("""select v.runprofile, 
				v.installprofile
				from nodes n, vm_nodes v where 
				n.id=v.node and
				n.name='%s'""" % host)
			for runProf, instProf in self.db.fetchall(): 
				self.addOutput(host, (runProf,instProf))

		self.endOutput(header=['host', 'runprofile', 'installprofile'])

