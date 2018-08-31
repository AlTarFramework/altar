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

# the mogi package meta-data
mogi.pkg.stem := mogi
mogi.pkg.root := models/mogi/mogi/
mogi.pkg.bin := models/mogi/bin/
mogi.pkg.pycdir := $(builder.dest.pyc)altar/models/mogi/
mogi.pkg.drivers := mogi

# end of file
