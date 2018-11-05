# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2018 all rights reserved
#

# project meta-data
emhp.major := 1
emhp.minor := 0

# use the altar area for build temporaries
emhp.tmpdir = $(altar.tmpdir)models/emhp/

# emhp consists of a python package
emhp.packages := emhp.pkg

# the emhp package meta-data
emhp.pkg.stem := emhp
emhp.pkg.root := models/emhp/emhp/
emhp.pkg.bin := models/emhp/bin/
emhp.pkg.pycdir := $(builder.dest.pyc)altar/models/emhp/
emhp.pkg.drivers := emhp

# end of file
