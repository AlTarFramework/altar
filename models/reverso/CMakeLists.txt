# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved

# get support
include(altar_reverso)

# build the package
altar_reverso_buildPackage()
# build the library
altar_reverso_buildLibrary()
# build the extension
altar_reverso_buildModule()
# copy the driver
altar_reverso_buildDriver()

# end of file
