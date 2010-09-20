# $Id: __init__.py,v 1.24 2010/09/20 17:55:50 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4 (Maverick)
# 
# Copyright (c) 2000 - 2010 The Regents of the University of California.
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
# Revision 1.24  2010/09/20 17:55:50  phil
# Allow VMs to define interfaces with no MAC addresses. In this case, do
# not bridge the interface in dom0.
#
# Revision 1.23  2010/09/07 23:53:33  bruno
# star power for gb
#
# Revision 1.22  2010/06/30 17:59:58  bruno
# can now route error messages back to the terminal that issued the command.
#
# can optionally set the VNC viewer flags.
#
# Revision 1.21  2009/10/12 21:12:39  bruno
# suppress error message when we boot a VM for the first time
#
# Revision 1.20  2009/06/01 23:38:30  bruno
# can use a physical partition for a VMs disk
#
# Revision 1.19  2009/05/06 16:37:12  bruno
# keep a xen domain up after a crash. helpful for debugging.
#
# Revision 1.18  2009/05/01 19:07:35  mjk
# chimi con queso
#
# Revision 1.17  2009/04/14 16:12:17  bruno
# push towards chimmy beta
#
# Revision 1.16  2009/04/08 22:27:58  bruno
# retool the xen commands to use libvirt
#
# Revision 1.15  2009/03/06 21:21:30  bruno
# updated for host attributes
#
# Revision 1.14  2009/01/16 23:58:15  bruno
# configuring the boot action and writing the boot files (e.g., PXE host config
# files and Xen config files) are now done in exactly the same way.
#
# Revision 1.13  2009/01/14 01:08:26  bruno
# kill the 'install=y' flag
#
# Revision 1.12  2009/01/14 00:20:56  bruno
# unify the physical node and VM node boot action functionality
#
# - all bootaction's are global
#
# - the node table has a 'runaction' (what bootaction should the node do when
#   a node normally boots) and an 'installaction (the bootaction for installs).
#
# - the 'boot' table has an entry for each node and it dictates what the node
#   will do on the next boot -- it will look up the runaction in the nodes table
#   (for a normal boot) or the installaction in the nodes table (for an install).
#
# Revision 1.11  2008/12/16 00:45:11  bruno
# merge vm_profiles and pxeaction tables into bootaction table
#
# Revision 1.10  2008/10/18 00:56:24  mjk
# copyright 5.1
#
# Revision 1.9  2008/09/25 17:56:54  bruno
# can't have spaces after the 'related' tag. otherwise, the xen usersguide
# will not build
#
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
import re

import sys
sys.path.append('/usr/lib64/python2.4/site-packages')
sys.path.append('/usr/lib/python2.4/site-packages')
import libvirt

#
# this function is used to suppress an error message when we start a VM
# for the very first time and there isn't a disk file created for it yet.
# the error message looks like:
#
#	libvir: Xen Daemon error : POST operation failed: (xend.err "Error
#	creating domain: Disk isn't accessible)"
#
def handler(ctxt, err):
	global errno

	errno = err


class Command(rocks.commands.start.host.command):
	"""
	Boots a VM slice on a physical node.

	<arg type='string' name='host' repeat='1'>
	A list of one or more VM host names.
	</arg>

	<example cmd='start host vm compute-0-0-0'>
	Start VM host compute-0-0-0.
	</example>

	<example cmd='start host vm compute-0-0-0'>
	Start VM host compute-0-0-0.
	</example>
	"""

	def getBridgeName(self, host, subnetid, vlanid):
		bridge = None

		if vlanid:
			#
			# first make sure the vlan is defined for the physical
			# host and get the logical subnet where the vlan is tied
			#
			rows = self.db.execute("""select net.subnet from
				networks net, nodes n where net.node = n.id and
				n.name = '%s' and (net.device like 'vlan%%' or
				net.device like '%%.%d') and
				net.vlanid = %d""" % (host, vlanid, vlanid))

			if rows == 0:
				self.abort('vlan %d not defined for host %s' %
					(vlanid, host))
			vlanOnLogical, = self.db.fetchone()

			rows = self.db.execute("""select net.device from
				networks net, nodes n where net.node = n.id
				and n.name = '%s' and
				net.device not like 'vlan%%' and
				net.subnet = %d""" % (host, vlanOnLogical))
		else:
			rows = self.db.execute("""select net.device from
				networks net, nodes n where net.node = n.id and
				n.name = '%s' and net.ip is not NULL and
				net.device not like 'vlan%%' and
				net.subnet = %d""" % (host, subnetid))
		if rows:
			dev, = self.db.fetchone()
			bridge = 'xenbr.%s' % (dev)
			if vlanid:
				reg = re.compile('.*\.%d' % vlanid)
				if not reg.match(dev):
					bridge = 'xenbr.%s.%d' % (dev, vlanid)

		return bridge

	def getXMLconfig(self, physhost, host):
		xmlconfig = []

		xmlconfig.append("<domain type='xen'>")
		xmlconfig.append("<name>%s</name>" % host)

		a = "<bootloader>/opt/rocks/bin/rocks-pygrub</bootloader>"
		xmlconfig.append(a)

		a = "<bootloader_args>--hostname=%s</bootloader_args>" % host
		xmlconfig.append(a)

		#
		# get the VM parameters
		#
		vmnodeid = None
		mem = None
		cpus = None
		slice = None
		macs = None
		disks = None

		rows = self.db.execute("""select vn.id, vn.mem, n.cpus
			from nodes n, vm_nodes vn where vn.node = n.id and
			n.name = '%s'""" % host)

		vmnodeid, mem, cpus = self.db.fetchone()
		if not vmnodeid or not mem or not cpus:
			return

		try:
			memory = int(mem) * 1024
		except:
			return

		xmlconfig.append("<memory>%s</memory>" % memory)	
		xmlconfig.append("<vcpu>%s</vcpu>" % cpus)	

		#
		# configure the devices
		#
		xmlconfig.append("<devices>")

		#
		# network config
		#
		rows = self.db.execute("""select net.mac, net.subnet, net.vlanid
			from networks net, nodes n, vm_nodes vn
			where vn.node = n.id and net.node = n.id and
			n.name = '%s' order by net.id""" % host)

		macs = self.db.fetchall()
		if not macs:
			return

		vifs = []
		index = 0
		for mac, subnetid, vlanid in macs:
			# allow VMs to have virtual and VLAN interfaces
			if mac is not None:
				xmlconfig.append("<interface type='bridge'>")
	
				bridge = self.getBridgeName(physhost, subnetid, vlanid)
				xmlconfig.append("<source bridge='%s'/>" % bridge)
				xmlconfig.append("<mac address='%s'/>" % mac)
				xmlconfig.append("<script path='vif-bridge'/>")
	
				xmlconfig.append("</interface>")
				index += 1

		#
		# disk config
		#
		rows = self.db.execute("""select vbd_type, prefix, name,
			device, mode, size from vm_disks where vm_node = %s
			order by id""" % vmnodeid)
		disks = self.db.fetchall()
		if not disks:
			return

		vmdisks = []
		index = 0
		bootdisk = None
		bootdevice = None
		for vbd_type,prefix,name,device,mode,size in disks:
			#
			# if the disk specification is a 'regular' file, then
			# make sure the file for the disk space exists. if
			# it doesn't, create a sparse file for the disk space.
			#
			file = os.path.join(prefix, name)

			if vbd_type in [ 'file', 'tap:aio' ]:
				a = "<disk type='file' device='disk'>"
				xmlconfig.append(a)

				if vbd_type == 'file':
					a = "<driver name='file'/>"
				elif vbd_type == 'tap:aio':
					a = "<driver name='tap' type='aio'/>"
				xmlconfig.append(a)

				a = "<source file='%s'/>" % file
				xmlconfig.append(a)

				a = "<target dev='%s'/>" % device
				xmlconfig.append(a)

				a = "</disk>"
				xmlconfig.append(a)

			elif vbd_type == 'phy':
				a = "<disk type='block' device='disk'>"
				xmlconfig.append(a)

				a = "<source dev='/dev/%s'/>" % name
				xmlconfig.append(a)

				a = "<target dev='%s'/>" % device
				xmlconfig.append(a)

				a = "</disk>"
				xmlconfig.append(a)
				
		#
		# the extra devices
		#
		xmlconfig.append("<input type='mouse' bus='xen'/>")
		xmlconfig.append("<graphics type='vnc' port='-1'/>")
		xmlconfig.append("<console tty='/dev/pts/0'/>")

		xmlconfig.append("</devices>")

		#
		# what to do on power on/off and crashes
		#
		xmlconfig.append("<on_poweroff>destroy</on_poweroff>")
		xmlconfig.append("<on_reboot>restart</on_reboot>")
		xmlconfig.append("<on_crash>preserve</on_crash>")

		xmlconfig.append("</domain>")

		return '\n'.join(xmlconfig)


	def bootVM(self, physhost, host, xmlconfig):
		hipervisor = libvirt.open('xen://%s/' % physhost)

		#
		# suppress an error message when a VM is started and
		# the disk file doesn't exist yet.
		#
		libvirt.registerErrorHandler(handler, 'context')

		retry = 0

		try:
			hipervisor.createLinux(xmlconfig, 0)
			self.command('set.host.boot',
				[ host, "action=os" ])
		except libvirt.libvirtError, m:
			str = '%s' % m
			if str.find("Disk isn't accessible") >= 1:
				#
				# the disk hasn't been created yet,
				# call a program to set them up, then
				# retry the createLinux()
				#
				cmd = 'ssh -q %s ' % physhost
				cmd += '/opt/rocks/bin/'
				cmd += 'rocks-create-vm-disks '
				cmd += '--hostname=%s' % host
				os.system(cmd)

				retry = 1
			else:
				print str

		if retry:
			hipervisor.createLinux(xmlconfig, 0)
			self.command('set.host.boot', [ host, "action=os" ])

		return


	def run(self, params, args):
		hosts = self.getHostnames(args)
		
		if len(hosts) < 1:
			self.abort('must supply at least one host')

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
			fout.write(self.command('report.host.vm', [ host ]))
			fout.close()
			os.system('scp -q %s %s:/etc/xen/rocks/%s' % 
				(temp, physhost, host))
			os.unlink(temp)

			#
			# get the VM configuration (in XML format for libvirt)
			#
			xmlconfig = self.getXMLconfig(physhost, host)

			#
			# boot the VM
			#
			self.bootVM(physhost, host, xmlconfig)

