# $Id: __init__.py,v 1.18 2011/07/23 02:31:44 phil Exp $
#
# @Copyright@
# 
# 				Rocks(r)
# 		         www.rocksclusters.org
# 		         version 5.4.3 (Viper)
# 
# Copyright (c) 2000 - 2011 The Regents of the University of California.
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
# 	Development Team at the San Diego Supercomputer Center at the
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
# Revision 1.18  2011/07/23 02:31:44  phil
# Viper Copyright
#
# Revision 1.17  2011/01/27 20:06:31  bruno
# tighten up the code
#
# Revision 1.16  2011/01/26 17:56:56  bruno
# new code to successfully add vlans dynamically on xen-based nodes
#
# Revision 1.15  2011/01/19 22:44:40  bruno
# no longer need 'rocks-create-vlan'.
#
# the xen folks have fixed their bug and now we can add vlans on-the-fly on a
# xen kernel just like you can on a non-xen kernel.
#
# Revision 1.14  2010/09/20 18:01:48  phil
# Move the service network restart from xenbrup to the main start stanza.
# Restart the network only once after all bridges have been built
#
# Revision 1.13  2010/09/07 23:53:33  bruno
# star power for gb
#
# Revision 1.12  2009/06/01 21:43:57  bruno
# restart the network after the xen bridge is created. this ensures our static
# routes are reconstituted
#
# Revision 1.11  2009/05/01 19:07:34  mjk
# chimi con queso
#
# Revision 1.10  2008/10/18 00:56:23  mjk
# copyright 5.1
#
# Revision 1.9  2008/09/25 17:39:55  bruno
# phil's command tweaks
#
# Revision 1.8  2008/09/22 18:14:57  bruno
# create the vlan, if needed
#
# Revision 1.7  2008/09/16 23:48:25  bruno
# make the rocks-network-bridge script dynamically determine the next
# free virtual interface
#
# Revision 1.6  2008/09/09 19:38:26  bruno
# don't build a bridge if there are no vlans specified
#
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

script = """<file name="/etc/xen/scripts/rocks-network-bridge" perms="755">
#!/bin/bash

get_vifnum () {
	GETVIFNUM=`brctl show | awk -v bname=$1 'BEGIN { insection = 0;
		brname = bname; }
	{
		if (match($1, "^" brname "$")) {
			if (split($1, a, ".") == 2) {
				insection = 1;
			}
		}
	}

	/vif/ {
		if (insection == 1) {
			if (split($1, a, ".") == 2) {
				print a[2];
			}
			insection = 0;
		}
	}'`
}

next_free_vifnum () {
	VIFNUM=`ifconfig -a | awk '/^veth/ {print $1}' | head -1 | sed -e 's/^veth//'`
}

xenbrup () {
	DEV=$1
	if [ "$2" != "" ]
	then
		DEV=$DEV.$2
	fi
	BRIDGE=xenbr.$DEV

	ip link show $BRIDGE > /dev/null 2>&amp;1
	if [ $? != 0 ]
	then
		#
		# check if the vlan is configured, if not, then configure it,
		# but before we configure it, make sure the physical bridge
		# is down
		#
		ip link show $DEV > /dev/null 2>&amp;1
		if [ $? != 0 -a "$2" != "" ]
		then
			ip link show xenbr.$1 > /dev/null 2>&amp;1
			if [ $? == 0 ]
			then
				get_vifnum xenbr.$1

				/etc/xen/scripts/network-bridge stop \\
					netdev=$1 bridge=xenbr.$1 \\
					vifnum=$GETVIFNUM
			fi

			/sbin/vconfig add $1 $2
		fi
		
		next_free_vifnum
		/etc/xen/scripts/network-bridge start netdev=$DEV \\
			bridge=$BRIDGE vifnum=$VIFNUM

	fi
}

case $1 in
start)
%s
	#
	# needed in order to ensure all our static routes are in place
	#
	/sbin/service network restart
	;;

esac
</file>
"""


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
			device = '%s' % (dev)

		return device
			

	def run(self, params, args):
		bridges = ''

		for host in self.getHostnames(args):
			#
			# order is important here -- we want all the vlan
			# bridges to be created first, then the bridge for
			# the physical interfaces. this is because when we
			# create a vlan on-the-fly (that is, not during the
			# first boot), then we must bring the physical bridge
			# down before we create the vlan. and by having the
			# physical bridge brought up last, we'll ensure the
			# physical bridge is restarted when we dynamically
			# create vlans.
			#

			#
			# create bridges for all VLANs
			#
			rows = self.db.execute("""select net.subnet, net.vlanid
				from networks net, nodes n where
				net.node = n.id and n.name = "%s" and
				net.vlanid is not NULL and
				net.device like 'vlan%%' order by net.id"""
				% (host))

			if rows > 0:
				for subnetid, vlanid in self.db.fetchall():
					device = self.getVlanDevice(host,
						subnetid, vlanid)

					bridges += '\txenbrup '
					bridges += '%s %s\n' \
						% (device, vlanid)

			#
			# create bridges for all physical interfaces that
			# are configured with an IP address
			#
			rows = self.db.execute("""select net.device from
				networks net, nodes n where net.node = n.id and
				n.name = "%s" and net.ip is not NULL and
				(net.vlanid is NULL or (net.vlanid is not NULL
				and net.device not like 'vlan%%'))
				order by net.id""" % (host))

			if rows > 0:
				for device, in self.db.fetchall():
					bridges += '\txenbrup %s\n' % (device)

		s = script % (bridges)
		self.addText(s)

