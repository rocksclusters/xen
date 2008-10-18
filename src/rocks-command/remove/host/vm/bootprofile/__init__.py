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
# Revision 1.2  2008/09/02 18:02:15  phil
# Improve check for removing global install profile
#
# Revision 1.1  2008/09/01 03:45:41  phil
# Remove a named vm bootprofile
#
#

import sys
import string
import rocks.commands
import os

class Command(rocks.commands.remove.host.command):
	"""
	Remove a boot/install profile from a list of hosts.

	<arg type='string' name='host' repeat='1'>
	List of hosts to remove profiles. If no hosts are listed,
	then the global definition that matches the 'profile=name' is removed.
	The global profile=install cannot be removed
	</arg>

	<param type='string' name='profile'>
	The label name for the profile to remove.  
	You can see the profiles available for
	a host by  executing: 'rocks list host vm profile &lt;hostname&gt;'.
	</param>

	<example cmd='remove host vm bootprofile compute-0-0-0 profile=boot'>
	Remove the 'boot' profile for compute-0-0-0.
	</example>
	"""

	def run(self, params, args):
		(profile, ) = self.fillParams([('profile', '%')])

		# If no host list is provided remove the default profile.
		# Otherwise remove the profile for each host.
		
		if not len(args):
			if profile.lower() == "install" or profile == "%":
				self.abort("Refusing to remove global install profile")
			self.db.execute("""delete from vm_profiles where
				vm_node=0 and vm_profiles.profile='%s'""" % profile)
		else:
			for host in self.getHostnames(args):
				self.db.execute("""delete from vm_profiles where
					vm_node=
					(select v.id from nodes n, vm_nodes v 
					where name='%s' and v.node = n.id)
					and vm_profiles.profile like '%s' """ % 
					(host, profile))
