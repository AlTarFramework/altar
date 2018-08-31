# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2018 all rights reserved
#

# project meta-data
gaussian.major := 1
gaussian.minor := 0

# use the altar area for build temporaries
gaussian.tmpdir = $(altar.tmpdir)/models/gaussian/

# gaussian consists of a python package
gaussian.packages := gaussian.pkg

# the gaussian package meta-data
gaussian.pkg.stem := gaussian
gaussian.pkg.root := models/gaussian/gaussian/
gaussian.pkg.bin := models/gaussian/bin/
gaussian.pkg.pycdir := $(builder.dest.pyc)altar/models/gaussian/
gaussian.pkg.drivers := gaussian

# end of file
