# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved

# get support
include(altar_gaussian)

# build the package
altar_gaussian_buildPackage()
# copy the driver
altar_gaussian_buildDriver()

# end of file
