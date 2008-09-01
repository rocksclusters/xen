# $Id: __init__.py,v 1.2 2008/09/01 04:07:34 phil Exp $
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
# Revision 1.2  2008/09/01 04:07:34  phil
# Profile a global flag to list only the global profiles.
#
# Revision 1.1  2008/09/01 03:41:13  phil
# Change from profile to bootprofile
#
# Revision 1.1  2008/08/31 06:03:43  phil
# Start of defining boot profiles
#

import sys
import socket
import rocks.commands
import string

class Command(rocks.commands.list.host.command):
	"""
	Lists the current VM Profiles available for hosts. 
	For each host supplied on the command line print the 
	hostname and defined profiles available to that host 
	
	The Profile describes the combination of kernel, ramdisk
        args that would be used if that profile where referenced for by the 
	Host as either a RunProfile or an InstallProfile
	Usually, the RunProfile is empty and the VM node will 
	boot from the kernel defined in its image. 

	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, info about
	all the known hosts is listed.
	</arg>

	<param optional='1' type='bool' name='global'>
 	If true, ignore the list of hosts and only return information about 
	global bootprofiles. Default is 'n'	
	</param>
	
	<example cmd='list host vm bootprofile compute-0-0-0'>
	List the profiles available to compute-0-0-0.
	</example>

	<example cmd='list host vm bootprofile'>
	List the profiles available for all known VM hosts.
	</example>

	<example cmd='list host vm bootprofile global=yes'>
	List only the globally-defined profiles without generating a list
	of hosts.
	</example>
	"""

	def  getVMHostnames(self, args, doGlobal):
		hosts=self.getHostnames(args)
		vmHosts = []
		if doGlobal:
			return vmHosts

		for host in hosts:
			self.db.execute("""select name from nodes, vm_nodes
				where vm_nodes.node=nodes.id 
				and nodes.name='%s'""" % host)
			for qhost in self.db.fetchall():
				vmHosts.append(qhost)
		return vmHosts

	def run(self, params, args):

		self.beginOutput()

		(doGlobal, ) = self.fillParams([('global','')])
         	doGlobal = self.str2bool(doGlobal)

		globalQuery = """select profile, kernel,
				ramdisk, args from 
				vm_profiles  where 
				vm_node=0 %s"""

		for host in self.getVMHostnames(args,doGlobal):
			# get profiles defined just for the node
			exclNodeProfiles = ''
			self.db.execute("""select p.profile, p.kernel,
				p.ramdisk, p.args from 
				nodes n, vm_nodes v, vm_profiles p where 
				p.vm_node=v.id and n.id=v.node and
				n.name='%s'""" % host)
			for profile, kern, ram, bootargs in self.db.fetchall(): 
				self.addOutput(host, (profile,kern,ram,bootargs))
				exclNodeProfiles += ' and profile != "%s" ' % profile	
			# now get the globals that we didn't pick up above
			self.db.execute(globalQuery % exclNodeProfiles)
			for profile, kern, ram, bootargs in self.db.fetchall(): 
				self.addOutput(host, (profile,kern,ram,bootargs))
		if doGlobal:
			# get the global actions 
			self.db.execute(globalQuery % '')
			for profile, kern, ram, bootargs in self.db.fetchall(): 
				self.addOutput('', (profile,kern,ram,bootargs))

		self.endOutput(header=['host', 'profile', 'kernel', 'ramdisk', 'args'])

