# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#

# default values for user choices
# source layout
src.py ?= $(project)
src.lib ?= lib
src.ext ?= ext
src.bin ?= bin

# destination layout
dest ?= $(prefix)
dest.py ?= $(dest)/packages
dest.lib ?= $(dest)/lib
dest.inc ?= $(dest)/include
dest.ext ?= $(dest.py)/$(project)/ext
dest.bin ?= $(dest)/bin
dest.staging ?= $(dest)/tmp

# recipes
$(dest) $(dest.bin) $(dest.py) $(dest.lib) $(dest.inc) $(dest.staging) :
	${call log.action,mkdir,$@}
	$(mkdirp) $@

# end of file
