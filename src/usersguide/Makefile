# 
# $Id: Makefile,v 1.13 2011/02/14 22:14:17 mjk Exp $
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
# $Log: Makefile,v $
# Revision 1.13  2011/02/14 22:14:17  mjk
# - Build Env
#   - ROLLNAME defaults to ROLL
#   - Fixes for docbook
# - All userguides build again
# - All userguides are now NOARCH rpms
#
# Revision 1.12  2010/09/07 23:53:34  bruno
# star power for gb
#
# Revision 1.11  2009/05/06 20:16:37  bruno
# build outside the source tree
#
# Revision 1.10  2009/05/01 19:07:35  mjk
# chimi con queso
#
# Revision 1.9  2008/10/18 00:56:25  mjk
# copyright 5.1
#
# Revision 1.8  2008/10/17 19:39:26  bruno
# xen doc touch ups
#
# Revision 1.7  2008/04/23 18:57:02  bruno
# basic structure in place
#
# Revision 1.6  2008/03/06 23:42:05  mjk
# copyright storm on
#
# Revision 1.5  2007/06/23 04:04:07  mjk
# mars hill copyright
#
# Revision 1.4  2006/09/11 22:50:50  mjk
# monkey face copyright
#
# Revision 1.3  2006/08/10 00:12:24  mjk
# 4.2 copyright
#
# Revision 1.2  2005/12/30 21:52:14  mjk
# *** empty log message ***
#
# Revision 1.1  2005/12/08 19:06:53  mjk
# start of xen roll
#
# Revision 1.7  2005/10/18 20:20:38  bruno
# automatically set the copyright date
#
# Revision 1.6  2005/10/12 18:11:08  mjk
# final copyright for 4.1
#
# Revision 1.5  2005/09/16 01:04:46  mjk
# updated copyright
#
# Revision 1.4  2005/05/24 21:23:59  mjk
# update copyright, release is not any closer
#
# Revision 1.3  2005/04/08 18:10:44  nadya
# move logic of creating rocks.dsl, rocks.css and stylesheet-images to Rules.mk
# which is copied from a single central location. Add target predoc in order to
# make docs in a local directory
#
# Revision 1.2  2005/01/18 16:28:09  fds
# Normalized stylesheets and stylesheet-images: no longer is rocks.dsl
# repeated for every roll by default. The pdf and html targets perform better
# when used on their own (for testing).
#
# Revision 1.1  2004/11/30 01:42:10  fds
# Normalize! This usersguide has a DOCROOT make var that pulls stylesheet-images
# and rocks.css, rocks.dsl from a central location in CVS. These are currently
# copied in several locations, namely rocks/src/roll/grid/src/usersguide, and
# rocks/src/roll/condor/src/usersguide among others.
#

PKGROOT         = /var/www/html/roll-documentation/xen/$(VERSION)
REDHAT.ROOT     = $(PWD)/../../


-include $(ROCKSROOT)/etc/Rules.mk
include Rules.mk

default: $(NAME).spec ../$(NAME)-$(VERSION).tar.gz

html: predoc
	jw --backend html --dsl $(PWD)/rocks.dsl#html index.sgml 

pdf: predoc
	jw --backend pdf --dsl $(PWD)/rocks.dsl#print index.sgml

build: html pdf

install:: build
	mkdir -p $(ROOT)/$(PKGROOT)/images
	mkdir -p $(ROOT)/$(PKGROOT)/stylesheet-images
	install -ma+r index.pdf 	$(ROOT)/$(PKGROOT)/$(NAME).pdf
	install -ma+r *.html    	$(ROOT)/$(PKGROOT)/
	install -ma+r images/*.png	$(ROOT)/$(PKGROOT)/images/
	install -ma+r stylesheet-images/{*.gif,*.png} \
		$(ROOT)/$(PKGROOT)/stylesheet-images/
	install -ma+r rocks.css $(ROOT)/$(PKGROOT)/

clean::
	rm -f *.html
	rm -f index.pdf


