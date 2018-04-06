# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# project
project := altar

# the source directory
src := .
# the destination directory
prefix := build
# the models
models := ${wildcard models/*}

# metadata
altar.major := 2
altar.minor := 0
altar.revision = ${strip ${shell $(bzr.revno) || echo 0}}
now.year = ${strip ${shell $(date.year)}}
now.date = ${strip ${shell $(date.stamp)}}

# recipes
all: altar $(models)

altar: project.package project.libraries

# recipes for building the models
$(models): project.package $(prefix)
	${call log.action,recurse,$@}
	$(MAKE) -C $@ -I ${realpath .} prefix=${realpath $(prefix)}

.PHONY: $(models)

# get the master makefile
include make/master.mm

# end of file
