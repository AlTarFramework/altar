# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved

# build the gaussian package
function(altar_gaussian_buildPackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY gaussian
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    gaussian/meta.py.in gaussian/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/gaussian
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(altar_gaussian_buildPackage)


# the scripts
function(altar_gaussian_buildDriver)
  # install the scripts
  install(
    PROGRAMS bin/gaussian
    DESTINATION bin
    )
  # all done
endfunction(altar_gaussian_buildDriver)

# end of file
