# -*- Makefile -*-
#
# Lijun Zhu
# Caltech
# (c) 2018 all rights reserved
#

# project meta-data
seismic.major := 1
seismic.minor := 0

# seismic consists of a python package
seismic.packages := seismic.pkg

# the seismic package meta-data
seismic.pkg.stem := seismic
seismic.pkg.root := models/seismic/seismic/
seismic.pkg.bin := models/seismic/bin/
seismic.pkg.pycdir := $(builder.dest.pyc)altar/models/seismic/
seismic.pkg.drivers := seismic

# end of file
