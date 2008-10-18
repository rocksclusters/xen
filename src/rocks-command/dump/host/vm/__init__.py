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
# Revision 1.2  2008/05/27 19:33:35  bruno
# touch up doc
#
# Revision 1.1  2008/04/21 16:36:54  bruno
# added dump command for restore roll
#
#

import os
import sys
import string
import rocks.commands

class Command(rocks.commands.dump.host.command):
	"""
	Dump host VM information as Rocks commands.
		
	<arg optional='1' type='string' name='host' repeat='1'>
	Zero, one or more host names. If no host names are supplied, 
	information for all hosts will be listed.
	</arg>

	<example cmd='dump host vm compute-0-0-0'>
	Dump VM info for compute-0-0-0.
	</example>

	<example cmd='dump host vm'>
	Dump VM info for all configured virtual machines.
	</example>
		
	<related>add host vm</related>
	"""

	def noSubnetsTable(self, params, args):
		for host in self.getHostnames(args):
                        rows = self.db.execute("""select
				net.device, net.mac, net.ip,
				net.netmask, net.gateway, net.module,
				net.name from
				networks net, nodes n
				where n.name = "%s" and net.node = n.id
				order by net.device""" % (host))

			if rows < 1:
				continue

			for (iface, mac, ip, netmask, gateway,
				module, name) in self.db.fetchall():
				
				if not iface:
					continue # nothing to dump
		
				self.dump('add host interface %s %s' % 
					(host, iface))

				set = 'set host interface %%s %s %s %%s' % \
					(host, iface)
				if ip:
					self.dump(set % ('ip', ip))
				if gateway:
					self.dump(set % ('gateway', gateway))
				if name:
					self.dump(set % ('name', name))
				if mac:
					self.dump(set % ('mac', mac))
				if module:
					self.dump(set % ('module', module))
				if iface == 'eth0':
					self.dump(set % ('subnet', 'private'))
				elif iface == 'eth1':
					self.dump(set % ('subnet', 'public'))

	def hasSubnetsTable(self, params, args):
		for host in self.getHostnames(args):
                        rows = self.db.execute("""select distinctrow
				IF(net.subnet, sub.name, NULL),
				net.device, net.mac, net.ip,
				IF(net.subnet, sub.netmask, NULL),
				net.gateway, net.module, net.name from
				nodes n, networks net, subnets sub
				where
				n.name='%s' and net.node=n.id and
				(net.subnet=sub.id or net.subnet is NULL)
				order by net.device""" % host )
			if rows < 1:
				continue
			for (subnet, iface, mac, ip, netmask, gateway,
				module, name) in self.db.fetchall():
				
				if not iface:
					continue # nothing to dump
		
				self.dump('add host interface %s %s' % 
					(host, iface))

				set = 'set host interface %%s %s %s %%s' % \
					(host, iface)
				if ip:
					self.dump(set % ('ip', ip))
				if gateway:
					self.dump(set % ('gateway', gateway))
				if name:
					self.dump(set % ('name', name))
				if mac:
					self.dump(set % ('mac', mac))
				if module:
					self.dump(set % ('module', module))
				if subnet:
					self.dump(set % ('subnet', subnet))


	def dumpVM(self, host):
		vmnodeid = None
		mem = None
		cpus = None
		slice = None
		macs = None
		disks = None
		physhost = None

		#
		# get the physical node that houses this VM
		#
		rows = self.db.execute("""select vn.physnode from
			vm_nodes vn, nodes n where n.name = '%s'
			and n.id = vn.node""" % (host))

		if rows == 1:
			physnodeid, = self.db.fetchone()
		else:
			#
			# not a VM
			#
			return

		rows = self.db.execute("""select name from nodes where
			id = %s""" % (physnodeid))

		if rows == 1:
			physhost, = self.db.fetchone()
		else:
			self.abort('cannot find a physical node "%s" ' +
				'for VM "%s"' % host)

		#
		# get the VM configuration parameters
		#
		rows = self.db.execute("""select vn.id, vn.mem,
			vn.slice, vn.virt_type from nodes n, vm_nodes vn
			where vn.node = n.id and n.name = '%s'""" %
			host)

		if rows != 1:
			self.abort('cannot find a configuration data ' +
				'for VM "%s"' % host)

		vmnodeid, mem, slice, virt_type = self.db.fetchone()

		disks = []
		disksizes = []
		rows = self.db.execute("""select vbd_type,
			prefix, name, device, mode, size from
			vm_disks where vm_node = %s""" %
			vmnodeid)

		if rows > 0:
			for vbd_type, prefix, name, device, mode, size in \
				self.db.fetchall():

				file = os.path.join(prefix, name)

				disk = '%s:%s,%s,%s' % (vbd_type, file,
						device, mode)
				disks.append(disk)
				disksizes.append('%d' % size)

		str = "set host vm %s physnode='%s' " % (host, physhost)
		str += "disk='%s' disksize='%s' " % \
			(' '.join(disks), ' '.join(disksizes))
		str += "mem='%d' slice='%d' virt-type='%s'" % \
			(mem, slice, virt_type)

		self.dump(str)


	def run(self, params, args):
		for host in self.getHostnames(args):
			self.dumpVM(host)

