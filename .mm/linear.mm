# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2018 all rights reserved
#

# project meta-data
linear.major := 1
linear.minor := 0

# use the altar area for build temporaries
linear.tmpdir = $(altar.tmpdir)/models/linear/

# linear consists of a python package
linear.packages := linear.pkg

# the linear package meta-data
linear.pkg.stem := linear
linear.pkg.root := models/linear/linear/
linear.pkg.bin := models/linear/bin/
linear.pkg.pycdir := $(builder.dest.pyc)altar/models/linear/
linear.pkg.drivers := linear

# end of file
