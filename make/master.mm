# -*- Makefile -*-
#
# michael a.g. aïvázis
# parasim
# (c) 1998-2018 all rights reserved
#

# defaults
include make/defaults/defaults.mm
# build diretory layout
include make/dest.mm
# stadard targets
include make/recipes.mm
# c++
include make/c++.mm
# python packages
include make/python.mm

# show me the default goal
default.info:
	$(log) default goal: ${.DEFAULT_GOAL}

# end of file
