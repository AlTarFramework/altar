# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2018 all rights reserved
#

# project meta-data
mogi.major := 1
mogi.minor := 0

# use the altar area for build temporaries
mogi.tmpdir = $(altar.tmpdir)models/mogi/

# mogi consists of a python package
mogi.packages := mogi.pkg
# a library
mogi.libraries = mogi.lib
# and an extension
mogi.extensions := mogi.ext

# the mogi package meta-data
mogi.pkg.stem := mogi
mogi.pkg.root := models/mogi/mogi/
mogi.pkg.bin := models/mogi/bin/
mogi.pkg.pycdir := $(builder.dest.pyc)altar/models/mogi/
mogi.pkg.drivers := mogi

# the mogi library metadata
mogi.lib.stem := mogi
mogi.lib.root := models/mogi/libmogi/
mogi.lib.incdir := $(builder.dest.inc)altar/models/mogi/
mogi.lib.c++.flags += $($(compiler.c++).std.c++17)

# the mogi extension meta-data
mogi.ext.stem := mogi
mogi.ext.root := models/mogi/extmogi/
mogi.ext.pkg := mogi.pkg
mogi.ext.wraps := mogi.lib
mogi.ext.extern := mogi.lib gsl pyre python
# compile options for the sources
mogi.ext.lib.c++.flags += $($(compiler.c++).std.c++17)

# end of file
