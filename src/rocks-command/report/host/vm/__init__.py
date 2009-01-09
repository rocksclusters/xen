# $Id: __init__.py,v 1.36 2009/01/09 20:42:51 bruno Exp $
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
# Revision 1.36  2009/01/09 20:42:51  bruno
# change pxeaction/pxeboot to bootaction/boot.
#
# Revision 1.35  2008/12/16 00:45:11  bruno
# merge vm_profiles and pxeaction tables into bootaction table
#
# Revision 1.34  2008/11/03 23:08:26  bruno
# phil's opensolaris xen fix
#
# Revision 1.33  2008/10/27 21:14:51  bruno
# get the disk creation size correct
#
# Revision 1.32  2008/10/18 00:56:23  mjk
# copyright 5.1
#
# Revision 1.31  2008/09/25 17:56:54  bruno
# can't have spaces after the 'related' tag. otherwise, the xen usersguide
# will not build
#
# Revision 1.30  2008/09/25 17:39:55  bruno
# phil's command tweaks
#
# Revision 1.29  2008/09/02 15:41:51  phil
# Support full disks (The Rocks Way) and a particular partition (Others)
#
# Revision 1.28  2008/09/01 18:50:04  phil
# Correctly write the host configuration file
#
# Revision 1.27  2008/09/01 18:28:33  phil
# Xen requires the disk to exist before calling bootloader. Put logic back into
# xen config to create, if it doesn't exist.  Remove this logic from rocks-pygrub
#
# Revision 1.26  2008/09/01 15:45:28  phil
# Use bootprofiles to determine how to boot this VM
#
# Revision 1.25  2008/08/29 21:16:54  phil
# Fix some parsing
#
# Revision 1.24  2008/08/29 19:00:12  phil
# use rocks-pygrub wrapper
#
# Revision 1.23  2008/08/28 02:37:25  phil
# Use pygrub for extracting the kernel from the image
#
# Revision 1.22  2008/08/14 19:32:05  phil
# properly retrieve the device name for mapping a vlan interface to the physical interface on which it is
# located
#
# Revision 1.21  2008/08/13 00:06:31  phil
# look for vlan interface names of the form vlan*
#
# Revision 1.20  2008/07/29 16:47:24  bruno
# more vlan support for xen VMs
#
# Revision 1.19  2008/07/22 00:16:20  bruno
# support for VLANs
#
# Revision 1.18  2008/07/01 22:57:08  bruno
# fixes to the xen reports which generate xen configuration files
#
# Revision 1.17  2008/04/25 17:17:17  bruno
# set the root to be the first partition on the boot disk and get the device
# name from the database
#
# Revision 1.16  2008/04/21 16:37:35  bruno
# nuked the vm_macs table -- now using the networks table to store/retrieve
# mac addresses for VMs
#
# Revision 1.15  2008/04/17 16:38:21  bruno
# incorporate phil's vm changes
#
# Revision 1.14  2008/04/15 23:08:13  bruno
# order the macs and disks
#
# Revision 1.13  2008/03/14 22:10:39  bruno
# touch up
#
# Revision 1.12  2008/03/06 23:42:04  mjk
# copyright storm on
#
# Revision 1.11  2008/02/27 17:43:24  bruno
# remove debug code
#
# Revision 1.10  2008/02/21 21:36:25  bruno
# get the mode correct
#
# Revision 1.9  2008/02/19 23:20:25  bruno
# katz made me do it.
#
# Revision 1.8  2008/02/12 00:01:26  bruno
# fixes
#
# Revision 1.7  2008/02/08 23:29:59  bruno
# tune
#
# Revision 1.6  2008/02/07 20:08:24  bruno
# retooled the commands and database tables to handle moving running VMs
#
# Revision 1.5  2008/02/01 21:38:54  bruno
# closer
#
# Revision 1.4  2008/01/30 22:01:35  bruno
# closer
#
# Revision 1.3  2008/01/30 00:54:32  bruno
# need to make 'create' a real boolean
#
# Revision 1.2  2008/01/29 01:22:00  bruno
# support forcing a reinstall of a VM
#
# Revision 1.1  2008/01/29 00:06:45  bruno
# changed 'rocks config' to 'rocks report'
#
# Revision 1.2  2007/12/10 20:59:25  bruno
# fixes to get a VMs configured and running on newly installed xen-based
# physical machines.
#
# Revision 1.1  2007/12/03 19:48:51  bruno
# xen for V
#
#

import os
import sys
import string
import re
import tempfile
import rocks.commands
import rocks.vm

header = """
import os
import os.path
import sys
"""

#### Strings that will be placed in .cfg file that drives rocks-pygrub
installConfig = """
installKernel = %s
installRamdisk = %s
installBootArgs = %s
"""
bootConfig = """
bootKernel = %s
bootRamdisk = %s
bootArgs = %s
"""

diskConfig =  """
disksize = % s
"""

forceConfig = """
forceInstall = True
"""
######
### Python Snippet that creates the cfgfile on the local 
### node. This drives rocks-pygrub so that it can switch 
### install vs. run state
writeConfigFile = """
cfgfile = "%s"
contents = %s

if not os.path.exists(bootdisk) or os.path.getsize(bootdisk) == 0:
        if not os.path.exists(os.path.dirname(bootdisk)):
                os.makedirs(os.path.dirname(bootdisk), 0700)
        cmd = 'dd if=/dev/zero of=%s bs=1 count=1 seek=%d > /dev/null 2>&1' 
        os.system(cmd)
        contents.append('forceInstall=True')

if not os.path.exists(cfgfile):
        if not os.path.exists(os.path.dirname(cfgfile)):
                os.makedirs(os.path.dirname(cfgfile), 0700)
cf = open(cfgfile,"w")
for line in contents:
     cf.write(line)
cf.close()
"""


runheader = """
#
# python code to extract the kernel from the disk image
#
bootloader = '/opt/rocks/bin/rocks-pygrub'
"""

linuxroot = """
root = "/dev/%s ro"
"""

trailer= """
vnc=1
vncpasswd=''
"""

class Command(rocks.commands.report.host.command):
	"""
	Outputs the VM configuration file for a slice on a physical node.
	
	<arg name='host' type='string'>
	One VM host name (e.g., compute-0-0-0).
	</arg>

	<param name='install' type='bool' optional='1'>
	If install='y' is set, then the VM will be first boot from
	its install bootprofile. Default is 'n'

	VMs use different mechanisms to control booting as compared to
	PXE-booted hosts. However, If the bootaction for a VM host is
	defined explicitly as "install*' for this VM, then
	this flag will be internally set to 'y'. 
	</param>

	<example cmd='report host vm compute-0-0-0'>
	Create the VM configuration file for host compute-0-0-0
	</example>

	<example cmd='report host vm compute-0-0-0 install=y'>
	Create the VM configuration file for host compute-0-0-0, and
	tell it to run its installprofile when it boots.
	</example>


	<related>set host vm boot</related>
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


	def getBootProfile(self, host, profile):
		"""Return what's defined by the named profile, Return
			string versions, empty strings if DB has Null entries"""

		kernel = '' 
		ramdisk =  ''
		bootargs = '' 
		if not profile:
			return kernel, ramdisk, bootargs

		# Read the global profile
		rows = self.db.execute("""select kernel, ramdisk, args
			from bootaction where action = '%s' and node = 0 """
			% profile)
		if rows > 0:
			kernel, ramdisk, bootargs = self.db.fetchone()

		# Read the local profile
		rows = self.db.execute("""select b.kernel, b.ramdisk, b.args
			from nodes n, bootaction b where
			b.action = '%s' and b.node = n.id and n.name = '%s'
			""" % (profile, host))

		if rows > 0:
			kernel, ramdisk, bootargs = self.db.fetchone()

		if not kernel:
			kernel = ''
		if not ramdisk:
			ramdisk = ''
		if not bootargs:
			bootargs = ''

		return kernel, ramdisk, bootargs


	def outputVMConfig(self, host, forceFlag):
		#
		# lookup the boot and run profiles for this VM host. 
		# Also look up the bootaction for this VM host.
		#      if the bootaction is like 'install%' force install
		#          on next boot
		
		# keep Track of what is going into the rocks-pygrub compatible
		# .cfg file 
		self.configContents = []

		# look up the names of the install and run profiles
		runProf = None
		instProf = None
		rows = self.db.execute("""select v.runprofile, v.installprofile
			from nodes n, vm_nodes v where n.name = '%s' and 
			n.id = v.node """ % host)
		if rows > 0:
			runProf, instProf, = self.db.fetchone()
		
		# boot profile
		kern, ramdsk, bootargs = self.getBootProfile(host, runProf)
		self.configContents.append(bootConfig % (kern, ramdsk,bootargs))

		# install profile
		kern, ramdsk, bootargs = self.getBootProfile(host, instProf)
		self.configContents.append(installConfig % (kern,
			ramdsk,bootargs))
		
		# Force Install?
		# look up the boot action
		bootaction = None
		rows = self.db.execute("""select b.action from boot b,
			nodes n where n.name = '%s' and n.id = b.node
			and action like 'install%%' """ % host)
		if rows > 0:
			bootaction, = self.db.fetchone()

		if bootaction or forceFlag:
			self.configContents.append(forceConfig)
	

		### Now get the other configuration file contents
		self.addOutput(host, header)
		self.addOutput(host, "name = '%s'" % host)

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

		#
		# get the VM disk specifications
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
				#
				# calculate how far to skip into
				# new output file
				#
				skip = int(size) * 1000 * 1000 * 1000
				self.configContents.append(diskConfig % skip)
				disksize = skip

			if not bootdisk:
				bootdisk = file
				bootdevice = device

			disk = "'%s:%s,%s,%s'" % (vbd_type, file, device, mode)
			vmdisks.append(disk)

		#
		# set the boot disk variable
		#
		if len(vmdisks) > 0:
			self.addOutput(host, "bootdisk = '%s'" % bootdisk)
			(basename,ext)= os.path.splitext(bootdisk)
			configFile = "%s.cfg" % basename
		else:
			self.abort('no disks specified')

		vm = rocks.vm.VM(self.db)
		physhost = vm.getPhysHost(host)
		if not physhost:
			self.abort('could not determine the physical host ' +
				'for host (%s)' % host)

		dirprefix = vm.getLargestPartition(physhost)

		if dirprefix:
			self.addOutput(host, "dirprefix = '%s'" % dirprefix)

		# Export Python Snippet that will create the local config file
		self.addOutput(host, 
			writeConfigFile % (configFile, self.configContents,
			bootdisk, (disksize - 1)))

		self.addOutput(host, runheader)

		self.addOutput(host, '#')
		self.addOutput(host, '# common config')
		self.addOutput(host, '#')

		self.addOutput(host, 'memory = %s' % mem)
		self.addOutput(host, 'vcpus = %s' % cpus)

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
			bridge = self.getBridgeName(physhost, subnetid, vlanid)
			vifs.append("'mac=%s, bridge=%s'" % (mac, bridge))
			index += 1

		self.addOutput(host, 'vif = [')
		self.addOutput(host, string.join(vifs, ',\n'))
		self.addOutput(host, ']')

		self.addOutput(host, 'disk = [')
		self.addOutput(host, string.join(vmdisks, ',\n'))
		self.addOutput(host, ']')

		# determine if file spec is raw disk, or a specific partition
		reg = re.compile('[\w/]+[\d]+')
		if not reg.match(bootdevice):
			bootdevice = bootdevice + "1"

		# if boot device is not a numerical device then
		reg = re.compile('^[\d]+')
		if not reg.match(bootdevice):
			self.addOutput(host, linuxroot % bootdevice)

		self.addOutput(host, trailer)

		self.addOutput(host, "on_reboot = 'restart'\n")

				
	def run(self, params, args):
		hosts = self.getHostnames(args)

                (forceInstall, ) = self.fillParams([('install','n')])
                forceInstall = self.str2bool(forceInstall)

		if len(hosts) < 1:
			self.abort('must supply host')

		self.beginOutput()
		for host in hosts:
			try:
				self.outputVMConfig(host, forceInstall)
			except TypeError:
				pass
		self.endOutput(padChar='')
	
