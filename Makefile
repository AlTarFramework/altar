# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2010-2018 california institute of technology
# (c) 2013-2018 parasim inc
# all rights reserved
#

# project
project := altar

# the source directory
src := .
# the destination directory
dest := build

# metadata
altar.major := 2
altar.minor := 0
altar.revision = ${strip ${shell $(bzr.revno) || echo 0}}
now.year = ${strip ${shell $(date.year)}}
now.date = ${strip ${shell $(date.stamp)}}

# recipes
all: python.pkg

# get the master makefile
include make/master.mm

# end of file
