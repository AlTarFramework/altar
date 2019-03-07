# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2010-2019 california institute of technology
# (c) 2013-2019 parasim inc
# all rights reserved
#

# project
project := emhp

# the source directory
src := .
# the destination directory
prefix ?= ../../build

# the emhp libraries
emhp.libraries :=

# destination layout
dest.py := $(prefix)/packages/altar/models
dest.lib := $(prefix)/lib
dest.ext := $(dest.py)/altar/models/$(project)/ext
dest.bin := $(prefix)/bin

# metadata
emhp.major := 2
emhp.minor := 0
emhp.revision = ${strip ${shell $(git.hash) || echo 0}}
now.year = ${strip ${shell $(date.year)}}
now.date = ${strip ${shell $(date.stamp)}}

# recipes
all: emhp

emhp: emhp.package emhp.libraries

# get the master makefile
include config/master.mm

# end of file
