# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#

# project
project := altar

# the source directory
src := .
# the destination directory
prefix := builds

# the altar libraries
altar.libraries := libaltar
# external dependencies
libaltar.packages := gsl pyre

# the altar extensions
altar.extensions := altarmodule
# external dependencies
altarmodule.packages := libaltarmodule libaltar gsl pyre python

# the models
models := ${wildcard models/*}
# the priors
priors := ${wildcard priors/*}

# metadata
altar.major := 2
altar.minor := 0
altar.revision = ${strip ${shell $(git.hash) || echo 0}}
now.year = ${strip ${shell $(date.year)}}
now.date = ${strip ${shell $(date.stamp)}}

# recipes
all: altar $(priors) $(models)

# make the altar python package, its libraries, and extensions
altar: altar.package altar.libraries altar.extensions

# recipes for building priors and models
$(priors) $(models) : altar
	${call log.info,recurse,$@}
	$(MAKE) -C $@ -I ${realpath .} prefix=${realpath $(prefix)}

# mark targets that are directories as phony
.PHONY: altar $(priors) $(models)

# get the master makefile
include config/master.mm

# end of file
