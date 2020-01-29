# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2010-2020 california institute of technology
# (c) 2013-2020 parasim inc
# all rights reserved
#

# project
project := gaussian

# the source directory
src := .
# the destination directory
prefix ?= ../../build

# the gaussian libraries
gaussian.libraries :=

# destination layout
dest.py := $(prefix)/packages/altar/models
dest.lib := $(prefix)/lib
dest.ext := $(dest.py)/altar/models/$(project)/ext
dest.bin := $(prefix)/bin

# metadata
gaussian.major := 2
gaussian.minor := 0
gaussian.revision = ${strip ${shell $(git.hash) || echo 0}}
now.year = ${strip ${shell $(date.year)}}
now.date = ${strip ${shell $(date.stamp)}}

# recipes
all: gaussian

gaussian: gaussian.package gaussian.libraries

# get the master makefile
include config/master.mm

# end of file
