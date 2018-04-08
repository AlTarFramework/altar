# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# defaults
include make/defaults/defaults.mm
# variables and recipes for building the destination directories
include make/dest.mm
# external packages
include make/packages.mm
# c++ compilations
include make/c++.mm
# python packages
include make/python.mm
# archives
include make/archives.mm
# extensions
include make/extensions.mm
# stadard targets
include make/recipes.mm

# end of file
