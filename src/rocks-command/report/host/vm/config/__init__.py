# $Id: __init__.py,v 1.7 2012/11/27 00:49:40 phil Exp $
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
# Revision 1.7  2012/11/27 00:49:40  phil
# Copyright Storm for Emerald Boa
#
# Revision 1.6  2012/05/06 05:49:50  phil
# Copyright Storm for Mamba
#
# Revision 1.5  2012/03/09 01:45:23  clem
# Rocks command xen is not compatible with 5.7 and 6.2
#
# Revision 1.4  2011/08/18 00:58:19  anoop
# Minor cleanup.
# Re-up the Release number
#
# Revision 1.3  2011/07/23 02:31:44  phil
# Viper Copyright
#
# Revision 1.2  2011/07/18 20:21:34  phil
# Give some diagnostics when creating a cluster.
# Support HVM_Features attribute to turn on/off services.
#
# Revision 1.1  2011/02/14 04:19:14  phil
# Now support HVM as well as paravirtual instances.
# Preliminary testing on 64bit complete.
#
#

import os
import tempfile
import rocks.commands
import re

import sys
sys.path.append('/usr/lib64/python2.' + str(sys.version_info[1]) + '/site-packages')
sys.path.append('/usr/lib/python2.' + str(sys.version_info[1]) + '/site-packages')
import libvirt

#
# this function is used to suppress an error message when we start a VM
# for the very first time and there isn't a disk file created for it yet.
# the error message looks like:
#
#	libvir: Xen Daemon error : POST operation failed: (xend.err "Error
#	creating domain: Disk isn't accessible)"
#
class Command(rocks.commands.report.host.command):
	"""
	Reports the XML Configuration for VM that will be handed
	to libvirt for startup.	

	<arg type='string' name='host' repeat='1'>
	One or more VM host names.
	</arg>

	<example cmd='report host vm config compute-0-0-0'>
	list the XML configuration of Report XML Config of VM compute-0-0-0.
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

	def reportBootLoader(self,host,xmlconfig,virtType):

		xmlconfig.append("<domain type='xen'>")
		xmlconfig.append("<name>%s</name>" % host)
		if virtType == 'hvm':
			xmlconfig.append("<os>")
			xmlconfig.append("<type>hvm</type>")
    			xmlconfig.append("<loader>/usr/lib/xen/boot/hvmloader</loader>")
			xmlconfig.append("<boot dev='network'/>")
			xmlconfig.append("<boot dev='hd'/>")
			xmlconfig.append("<bootmenu enable='yes'/>")
			xmlconfig.append("</os>")

		else:
			a = "<bootloader>/opt/rocks/bin/rocks-pygrub</bootloader>"
			xmlconfig.append(a)
			a = "<bootloader_args>--hostname=%s</bootloader_args>" % host
			xmlconfig.append(a)

	def getXMLconfig(self, physhost, host):
		xmlconfig = []
		virtType = self.command('report.host.vm.virt_type', [ host,]).strip()
		self.reportBootLoader(host,xmlconfig,virtType)
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

		if virtType == 'hvm':
			features = self.db.getHostAttr(host,'HVM_Features')
			if features is None :
				features = """\t<acpi/>\n\t<apic/>\n\t<pae/>"""
			xmlconfig.append("<features>")
			xmlconfig.append(features)
			xmlconfig.append("</features>")

		#
		# configure the devices
		#
		xmlconfig.append("<devices>")
		if virtType == 'hvm':
			if self.arch == 'x86_64':
				xmlconfig.append("  <emulator>/usr/lib64/xen/bin/qemu-dm</emulator>")
			else:
				xmlconfig.append("  <emulator>/usr/lib/xen/bin/qemu-dm</emulator>")

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
				xmlconfig.append("  <interface type='bridge'>")
	
				bridge = self.getBridgeName(physhost, subnetid, vlanid)
				xmlconfig.append("    <source bridge='%s'/>" % bridge)
				xmlconfig.append("    <mac address='%s'/>" % mac)
				xmlconfig.append("    <script path='vif-bridge'/>")
	
				xmlconfig.append("  </interface>")
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

		if virtType != 'hvm':
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



	def run(self, params, args):
		hosts = self.getHostnames(args)
		
		if len(hosts) < 1:
			self.abort('must supply at least one host')

		self.beginOutput()
		for host in hosts:
			#
			# get the VM configuration (in XML format for libvirt)
			#

			rows = self.db.execute("""select name from nodes where
				id=(select vn.physnode from
				vm_nodes vn, nodes n where n.name = '%s'
				and n.id = vn.node)""" % (host))
			if rows == 1:
				physhost, = self.db.fetchone()
			else:
				continue

			xmlconfig = self.getXMLconfig(physhost, host)
			self.addOutput(host, '%s' % xmlconfig)

		self.endOutput(padChar='')
	

