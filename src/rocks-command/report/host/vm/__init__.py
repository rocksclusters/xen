# $Id: __init__.py,v 1.18 2008/07/01 22:57:08 bruno Exp $
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
"""

installheader = """
kernel = "/boot/kickstart/xen/vmlinuz"
ramdisk = "/boot/kickstart/xen/initrd-xen.iso.gz"
extra = "%s"
"""

runheader = """
#
# python code to extract the kernel from the disk image
#
kernelsdir = os.path.join(dirprefix, 'xen/kernels')

cmd = 'mkdir -p /mnt/disk'
os.system(cmd)
cmd = 'mkdir -p %s' % kernelsdir
os.system(cmd)

cmd = 'lomount -diskimage %s -partition 1 /mnt/disk' % bootdisk
os.system(cmd)

kernel = os.path.join(kernelsdir, 'vmlinuz-%s' % (name))
ramdisk = os.path.join(kernelsdir, 'initrd-%s' % (name))

cmd = 'cp /mnt/disk/boot/vmlinuz* %s' % kernel
os.system(cmd)

cmd = 'cp /mnt/disk/boot/initrd* %s' % ramdisk
os.system(cmd)

os.system('umount /mnt/disk')
"""

diskcreate = """
#
# create a sparse file for a local disk image
#
diskfile = '%s'
if not os.path.exists(diskfile):
	if not os.path.exists(os.path.dirname(diskfile)):
		os.makedirs(os.path.dirname(diskfile), 0700)

	cmd = 'dd if=/dev/zero of=%s bs=1 count=1 seek=%d > /dev/null 2>&1'
	os.system(cmd)
"""

trailer = """
root = "/dev/%s1 ro"

vnc=1
vncpasswd=''
"""

class Command(rocks.commands.report.host.command):
	"""
	Outputs the VM configuration file for a slice on a physical node.
	
	<arg name='host' type='string'>
	One VM host name (e.g., compute-0-0-0).
	</arg>

	<example cmd='report host vm compute-0-0-0'>
	Outputs a configuration file for the VM host compute-0-0-0.
	</example>
	"""

	def outputVMConfig(self, host):
		#
		# lookup the pxeboot action for this VM host. if the action is
		# 'os', then output a configuration file that puts the VM host
		# into 'normal boot' mode.
		#
		# otherwise, assume it is an installation and output a
		# configuration file that will put the  VM host into
		# installation mode.
		#
		#
		action = None
		rows = self.db.execute("""select p.action from pxeboot p,
			nodes n where n.name = '%s' and n.id = p.node""" % host)

		if rows > 0:
			action, = self.db.fetchone()

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
				skip -= 1

				self.addOutput(host, diskcreate % (file, file,
					skip))

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

		if not action:
			action = 'install'

		if action == 'os':
			self.addOutput(host, runheader)
		else:
			#
			# default kernel parameters
			#
			extra = "client kssendmac ks ksdevice=eth0 " + \
				"selinux=0 ramdisk_size=150000 noipv6 ekv"

			rows = self.db.execute("""select p.args from
				pxeaction p, nodes n where n.name = "%s" and
				n.id = p.node and p.action = "%s" """ %
				(host, action))

			if rows < 1:
				#
				# get the global specification
				#
				rows = self.db.execute("""select args from
					pxeaction where node = 0 and
					action = "%s" """ % action)

			if rows > 0:
				extra, = self.db.fetchone()

			self.addOutput(host, installheader % extra)

		self.addOutput(host, '#')
		self.addOutput(host, '# common config')
		self.addOutput(host, '#')

		self.addOutput(host, 'memory = %s' % mem)
		self.addOutput(host, 'vcpus = %s' % cpus)

		rows = self.db.execute("""select net.mac 
			from networks net, nodes n, vm_nodes vn
			where vn.node = n.id and net.node = n.id and
			n.name = '%s'""" % host)

		macs = self.db.fetchall()
		if not macs:
			return

		vifs = []
		index = 0
		for mac, in macs:
			vifs.append("'mac=%s, bridge=xenbr%d'" % (mac, index))
			index += 1
		self.addOutput(host, 'vif = [')
		self.addOutput(host, string.join(vifs, ',\n'))
		self.addOutput(host, ']')

		self.addOutput(host, 'disk = [')
		self.addOutput(host, string.join(vmdisks, ',\n'))
		self.addOutput(host, ']')

		self.addOutput(host, trailer % bootdevice)

		if action == 'os':
			self.addOutput(host, "on_reboot = 'restart'\n")
		else:
			self.addOutput(host, "on_reboot = 'destroy'\n")

				
	def run(self, params, args):
		hosts = self.getHostnames(args)
		
		if len(hosts) < 1:
			self.abort('must supply host')

		self.beginOutput()
		for host in hosts:
			try:
				self.outputVMConfig(host)
			except TypeError:
				pass
		self.endOutput(padChar='')
	
