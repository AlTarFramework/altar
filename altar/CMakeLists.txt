# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved

# get support
include(altar_framework)

# build the package
altar_buildPackage()
# build the library
altar_buildLibrary()
# build the extension
altar_buildModule()
# copy the driver
altar_buildDriver()

# end of file
