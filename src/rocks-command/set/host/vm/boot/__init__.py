# $Id: __init__.py,v 1.2 2008/10/18 00:56:24 mjk Exp $
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
# Revision 1.2  2008/10/18 00:56:24  mjk
# copyright 5.1
#
# Revision 1.1  2008/09/01 05:23:00  phil
# Set the run/install bootprofile for a VM
#
#

import rocks.commands
import string

class Command(rocks.commands.set.host.command):
	"""
	Set the install/run bootprofile for a vm host. 
	This bootprofile defines what configuration
	is used to boot a vm in its running and/or installing configuration 
	
	<arg type='string' name='host' repeat='1'>
	One or more host names.
	</arg>

	<param type='string' name='installprofile' optional='1'>
	The label name for the bootprofile to use when installing a node. 
	For a list of available bootprofiles,
	execute: 'rocks list host vm bootprofile &lt;hostname&gt;'.
	It is an error to set the install profile to None.
	</param>
		
	<param type='string' name='runprofile' optional='1'>
	The label name for the bootprofile to use when a node is running'
	normally. Usually this is empty, and the kernel defined inside of 
	the VM will be used for booting.  
	For a list of bootprofiles,
	execute: 'rocks list host vm bootprofile &lt;hostname&gt;'.
	Set this string to 'None' to clear the run profile
	</param>
		
	<example cmd='set host vm boot compute-0-0-0 installprofile=install'>
	Set the 'install' bootprofile for compute-0-0-0, when installing it.
	</example>

	<example cmd='set host vm boot compute-0-0-0 runprofile=None'>
	clear the 'run' runprofile for compute-0-0-0, and use the kernel
	defined in the VM image,
	</example>
	"""

	def setProfile(self, vm_nodeid, host, profile, instOrRun):
		#
		# just make sure there is a profile of the name this host.
		# we will not be using the result from the query, we just
		# want to know if the profile exists for this host.
		#
		query = """select Profile from vm_profiles where
			(Vm_Node = %s or Vm_Node = 0) 
			and Profile = "%s" """ % (vm_nodeid, profile)
		rows = self.db.execute(query)

		if profile and rows < 1:
			self.abort('VM boot profile' + 
				'(%s) is not defined ' % (profile) +
				'for host (%s)' % (host))
		
		# construct the query and updated
		query = 'update vm_nodes set %s=' %instOrRun 
		if profile:
			query = query + '"%s"' % profile
		else:
			query = query + 'NULL' 

		query = query + ' where id=%s' % vm_nodeid
		self.db.execute(query)

	def run(self, params, args):
		(runProf,instProf) = self.fillParams([('runprofile','' ),
					('installprofile','')])

		if string.lower(runProf) == "none":
			runProf = None
		if string.lower(instProf) == "none":
			instProf = None

		for host in self.getHostnames(args):
			#
			# get the nodeid from the nodes table
			#
			rows= self.db.execute("""select v.id
				from nodes n, vm_nodes v 
				where n.name = '%s' and
				n.id = v.node""" % host)

			if rows:
				vm_nodeid,  = self.db.fetchone()
				if vm_nodeid and runProf != '':
					self.setProfile(vm_nodeid, host, 
						runProf,'RunProfile')

				if vm_nodeid and instProf:
					self.setProfile(vm_nodeid, host, 
						instProf,'InstallProfile')
