# $Id: __init__.py,v 1.5 2008/07/29 16:47:25 bruno Exp $
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
# Revision 1.5  2008/07/29 16:47:25  bruno
# more vlan support for xen VMs
#
# Revision 1.4  2008/07/22 00:16:20  bruno
# support for VLANs
#
# Revision 1.3  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.2  2008/01/29 01:22:05  bruno
# fix
#
# Revision 1.1  2008/01/29 00:06:45  bruno
# changed 'rocks config' to 'rocks report'
#
# Revision 1.1  2007/12/03 19:48:51  bruno
# xen for V
#
#

import rocks.commands

class Command(rocks.commands.report.host.command):
	"""
	Generates the Xen networking bridge configuration script for a
	host.
	
	<example cmd="report host xen bridge">
	</example>
	"""
		
	def getVlanDevice(self, host, subnetid, vlanid):
		device = None

		rows = self.db.execute("""select net.device from networks net,
			nodes n where net.node = n.id and n.name = '%s' and
			net.ip is not NULL and net.device not like 'vlan%%' and
			net.subnet = %d""" % (host, subnetid))

		if rows:
			dev, = self.db.fetchone()
			device = '%s.%d' % (dev, vlanid)

		return device
			

	def addNetworkBridge(self, device, vifnum):
		self.addText('/etc/xen/scripts/network-bridge ' +
			'"$@" netdev=%s bridge=xenbr.%s vifnum=%d\n' 
			% (device, device, vifnum))
		

	def run(self, params, args):
		self.addText('<file ' +
			'name="/etc/xen/scripts/rocks-network-bridge" ' +
			'perms="755">\n')
		self.addText('#!/bin/bash\n')

		for host in self.getHostnames(args):
			vifnum = 0

			#
			# create bridges for all physical interfaces that
			# are configured with an IP address
			#
			rows = self.db.execute("""select net.device from
				networks net, nodes n where net.node = n.id and
				n.name = "%s" and net.ip is not NULL and
				net.vlanid is NULL order by net.id""" % (host))

			for device, in self.db.fetchall():
				self.addNetworkBridge(device, vifnum)
				vifnum += 1

			#
			# create bridges for all VLANs
			#
			rows = self.db.execute("""select net.subnet, net.vlanid
				from networks net, nodes n where
				net.node = n.id and n.name = "%s" and
				net.vlanid is not NULL and
				net.device like 'vlan%%' order by net.id"""
				% (host))

			for subnetid, vlanid in self.db.fetchall():
				device = self.getVlanDevice(host, subnetid,
					vlanid)
				self.addNetworkBridge(device, vifnum)
				vifnum += 1

		self.addText('</file>')

