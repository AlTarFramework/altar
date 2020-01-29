# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#

# defaults
include config/defaults/defaults.mm
# variables and recipes for building the destination directories
include config/dest.mm
# build system
include config/mm.mm
# external packages
include config/packages.mm
# c++ compilations
include config/c++.mm
# python packages
include config/python.mm
# archives
include config/archives.mm
# extensions
include config/extensions.mm
# stadard targets
include config/recipes.mm
# pull it all together
include config/project.mm

# end of file
