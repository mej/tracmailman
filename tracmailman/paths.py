# -*- python -*-

# Copyright (C) 1998-2007 by the Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301,
# USA.

# This file becomes paths.py which is installed in may directories.  By
# importing this module, sys.path gets `hacked' so that the $prefix/Mailman
# directory is inserted at the start of that list.  That directory really
# contains the Mailman modules in package form.  This file exports two
# attributes that other modules may use to get the absolute path to the
# installed Mailman distribution.

import os
import sys
from warnings import filterwarnings

# some scripts expect this attribute to be in this module
prefix = '/var/lib/mailman'
exec_prefix = '${prefix}'

# work around a bogus autoconf 2.12 bug
if exec_prefix == '${prefix}':
    exec_prefix = prefix

# Supress Python 2.5 warning about string exceptions.
filterwarnings('ignore', '.* string exception', DeprecationWarning)

# Check if ja/ko codecs are available before changing path.
try:
    s = unicode('OK', 'iso-2022-jp')
    jaok = True
except LookupError:
    jaok = False

try:
    s = unicode('OK', 'euc-kr')
    kook = True
except LookupError:
    kook = False

# Hack the path to include the parent directory of the $prefix/Mailman package
# directory.
sys.path.insert(0, prefix)

# We also need the pythonlib directory on the path to pick up any overrides of
# standard modules and packages.  Note that these must go at the front of the
# path for this reason.
sys.path.insert(0, os.path.join(prefix, 'pythonlib'))

# Include Python's site-packages directory.
sitedir = os.path.join(sys.prefix, 'lib', 'python'+sys.version[:3],
                       'site-packages')
sys.path.append(sitedir)


# In a normal interactive Python environment, the japanese.pth and korean.pth
# files would be imported automatically.  But because we inhibit the importing
# of the site module, we need to be explicit about importing these codecs.
if not jaok:
    try:
        import japanese
    except ImportError:
        pass
# As of KoreanCodecs 2.0.5, you had to do the second import to get the Korean
# codecs installed, however leave the first import in there in case an upgrade
# changes this.
if not kook:
    try:
        import korean
        import korean.aliases
    except ImportError:
        pass
# Arabic and Hebrew (RFC-1556) encoding aliases. (temporary solution)
import encodings.aliases
encodings.aliases.aliases.update({
    'iso_8859_6_e': 'iso8859_6',
    'iso_8859_6_i': 'iso8859_6',
    'iso_8859_8_e': 'iso8859_8',
    'iso_8859_8_i': 'iso8859_8',
})
