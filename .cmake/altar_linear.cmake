# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved

# build the linear package
function(altar_linear_buildPackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY linear
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    linear/meta.py.in linear/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/linear
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(altar_linear_buildPackage)


# the scripts
function(altar_linear_buildDriver)
  # install the scripts
  install(
    PROGRAMS bin/linear
    DESTINATION bin
    )
  # all done
endfunction(altar_linear_buildDriver)

# end of file
