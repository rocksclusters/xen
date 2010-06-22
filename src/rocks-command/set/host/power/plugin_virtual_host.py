# $Id: plugin_virtual_host.py,v 1.1 2010/06/22 21:41:14 bruno Exp $
# 
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		       version 5.2 (Chimichanga)
# 
# Copyright (c) 2000 - 2009 The Regents of the University of California.
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
# $Log: plugin_virtual_host.py,v $
# Revision 1.1  2010/06/22 21:41:14  bruno
# basic control of VMs from within a VM
#
#

import rocks.commands
import rocks.vm

class Plugin(rocks.commands.Plugin):

	def provides(self):
		return 'virtual-host'

	def run(self, args):
		host = args[0]
		state = args[1]
		key = args[2]

		#
		# if 'vm-controller' is set, then we assume this is a virtual
		# frontend and we want to send a command to the VM controller
		# for this virtual cluster.
		#
		vm_controller = self.db.getHostAttr('localhost',
			'vm-controller')
		if vm_controller:
			me = self.db.getHostname()
			vm = rocks.vm.VMControl(self.db, me, vm_controller)

			if state == 'on':
				op = 'power on'
			elif state == 'off':
				op = 'power off'

			if vm.cmd(op, host) == 'failed':
				self.abort('command failed')
		else:
			#
			# determine if this is a virtual host
			#
			virtnode = 1

			rows = self.db.execute("""show tables like
				'vm_nodes' """)

			if rows == 1:
				rows = self.db.execute("""select vn.id from
					vm_nodes vn, nodes n where
					vn.node = n.id and
					n.name = "%s" """ % (host))
				if rows == 1:
					virtnode = 0
