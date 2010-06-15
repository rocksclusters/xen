# $Id: __init__.py,v 1.1 2010/06/15 19:38:45 bruno Exp $
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
# $Log: __init__.py,v $
# Revision 1.1  2010/06/15 19:38:45  bruno
# start/stop the vmcontrol service
#
#

import socket
import POW
import os
import sys
import rocks.vm
import rocks.commands
import MySQLdb

#
# 'V' 'M' -- 86, 77 is decimal representation of 'V' 'M' in ASCII
#
port = 8677

class Command(rocks.commands.start.service.command):
	"""
	Starts the VM Control service. This service validates commands from
	remote hosts and, if the command is accepted, the command is parsed
	and applied to VMs that are managed by this host.
	"""

	def reconnect(self):
		#
		# reconnect to the database
		#

		# First try to read the cluster password (for apache)

		passwd = ''

		try:
			file = open('/opt/rocks/etc/my.cnf','r')
			for line in file.readlines():
				l = line[:-1].split('=')
				if len(l) > 1 and l[0] == "password":
					passwd = l[1]	
					break
			file.close()
		except:
			pass

		try:
			host = rocks.DatabaseHost
		except:
			host = 'localhost'

		# Now make the connection to the DB

		try:
			if os.geteuid() == 0:
				username = 'apache'
			else:
				username = pwd.getpwuid(os.geteuid())[0]

			# Connect over UNIX socket if it exists, otherwise go
			# over the network.

			if os.path.exists('/var/opt/rocks/mysql/mysql.sock'):
				Database = MySQLdb.connect(db='cluster',
					host='localhost',
					user=username,
					passwd='%s' % passwd,
					unix_socket='/var/opt/rocks/mysql/mysql.sock')
			else:
				Database = MySQLdb.connect(db='cluster',
					host='%s' % host,
					user=username,
					passwd='%s' % passwd,
					port=40000)

		except ImportError:
			Database = None
		except OperationalError:
			Database = None
	
		return (Database)


	def listmacs(self, ssl, frontend):
		#
		# return a list of all the MACs associated with this cluster
		#
		macs = []

		vm = rocks.vm.VM(self.db)
		if vm.isVM(frontend):
			#
			# all client nodes of this VM frontend have
			# the same vlan id as this frontend
			#
			rows = self.db.execute("""select
				net.vlanid from
				networks net, nodes n, subnets s where
				n.name = '%s' and net.node = n.id and
				s.name = 'private' and
				s.id = net.subnet""" % frontend)

			if rows > 0:
				vlanid, = self.db.fetchone()

				rows = self.db.execute("""select n.name,
					net.mac from networks net, nodes n
					where net.vlanid = %s and
					net.node = n.id""" % vlanid)

				for client, mac in self.db.fetchall():
					if vm.isVM(client):
						macs.append(mac)

		msg = ''
		for m in macs:
			msg += '%s\n' % m

		ssl.write('%08d\n' % len(msg))
		ssl.write(msg)


	def parse_msg(self, buf):
		b = buf.split('\n')

		op = b[0].strip()
		src_mac = b[1].strip()

		if len(b) == 3:
			dst_mac = b[2].strip()
		else:
			dst_mac = ''

		return (op, src_mac, dst_mac)


	def check_signature(self, frontend, clear_text, signature):
		if not frontend:
			return 0

		digest = POW.Digest(POW.RIPEMD160_DIGEST)
		digest.update(clear_text)

		rows = self.db.execute("""select public_key from 
			public_keys where node = (select id from nodes
			where name = '%s') """ % frontend)

		if rows == 0:
			return 0

		for public_key, in self.db.fetchall():
			key = POW.pemRead(POW.RSA_PUBLIC_KEY, public_key)

			if key.verify(signature, digest.digest(), \
					POW.RIPEMD160_DIGEST):
				return 1

		return 0


	def daemonize(self):
		#
		# The python Daemon dance. From Steven's "Advanced Programming
		# in the UNIX env".
		#
		pid = os.fork()
		if pid > 0:
			sys.exit(0)

		#
		# now decouple from parent environment
		#

		#
		# So we can remove/unmount the dir the daemon started in.
		#
		os.chdir("/")

		#
		# Create a new session and set the process group.
		#
		os.setsid()
		os.umask(0)

		#
		# do a second fork
		#
		pid = os.fork()
		if pid > 0:
			#
			# exit from second parent
			#
			sys.exit(0)

		#
		# redirect standard file descriptors
		#
		sys.stdout.flush()
		sys.stderr.flush()
		si = file('/dev/null', 'r')
		so = file('/var/log/vm-control.log', 'a+')
		se = so
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())


	def run(self, params, args):
		self.daemonize()

		#
		# after this program becomes a daemon, we need to get a new
		# connect to the database. that is because the parent closes
		# the initial database connection
		#
		database = self.reconnect()

		if not database:
			self.abort("couldn't connect to the database")

		self.db.database = database
		self.db.link = database.cursor()

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('', port))
		s.listen(1)

		#
		# read the key/cert
		#
		keyfile = open('/etc/pki/libvirt/private/serverkey.pem', 'r')
		certfile = open('/etc/pki/libvirt/servercert.pem', 'r')

		rsa = POW.pemRead(POW.RSA_PRIVATE_KEY, keyfile.read())
		x509 = POW.pemRead(POW.X509_CERTIFICATE, certfile.read())

		keyfile.close()
		certfile.close()

		ssl = POW.Ssl(POW.SSLV23_SERVER_METHOD)
		ssl.useCertificate(x509)
		ssl.useKey(rsa)

		done = 0
		while not done:
			conn, addr = s.accept()

			print 'received message from: ', addr
			sys.stdout.flush()

			ssl.setFd(conn.fileno())
			ssl.accept()

			#
			# read the length of the clear text
			#
			buf = ssl.read(9)

			try:
				clear_text_len = int(buf)
			except:
				continue

			#
			# now read the clear text
			#
			clear_text = ''
			while len(clear_text) != clear_text_len:
				msg = ssl.read(clear_text_len - len(clear_text))
				clear_text += msg

			(op, src_mac, dst_mac) = self.parse_msg(clear_text) 

			print '\top:\t\t%s' % op
			print '\tsrc_mac:\t%s' % src_mac
			print '\tdst_mac:\t %s' % dst_mac
			sys.stdout.flush()

			frontend = self.db.getHostname(src_mac)

			#
			# get the digital signature
			#
			buf = ssl.read(9)

			try:
				signature_len = int(buf)
			except:
				continue

			signature = ''
			while len(signature) != signature_len:
				msg = ssl.read(signature_len - len(signature))
				signature += msg

			#
			# check the signature
			#
			if self.check_signature(frontend, clear_text,
					signature):
				print '\tmessage signature is valid'
				sys.stdout.flush()

				if op == 'power off':
					self.command('stop.host.vm',
						[ dst_mac ] )
				elif op == 'power on':
					self.command('start.host.vm',
						[ dst_mac ] )
				elif op == 'list macs':
					self.listmacs(ssl, frontend)
			else:
				print '\tmessage signature is invalid'
				sys.stdout.flush()

				#
				# for the commands that require a response
				# we need to send back an empty message so
				# the remote client won't hang.
				#
				if op == 'list macs':
					ssl.write('%08d\n' % 0)

