# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved

# get support
include(altar_cdm)

# build the package
altar_cdm_buildPackage()
# build the library
altar_cdm_buildLibrary()
# build the extension
altar_cdm_buildModule()
# copy the driver
altar_cdm_buildDriver()

# end of file
