# -*- Makefile -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#

# be quiet
.SILENT:
# shutdown make's implict rule database
.SUFFIXES:
# set the default goal so we don't depend on presentation order
.DEFAULT_GOAL = all

# initialize the various categories of variables
# tokens
include config/defaults/tokens.mm
# tools
include config/defaults/tools.mm
# help
include config/defaults/log.mm

# end of file
