# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved



# build the emhp package
function(altar_emhp_buildPackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY emhp
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    emhp/meta.py.in emhp/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/emhp
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(altar_emhp_buildPackage)


# the scripts
function(altar_emhp_buildDriver)
  # install the scripts
  install(
    PROGRAMS bin/emhp
    DESTINATION bin
    )
  # all done
endfunction(altar_emhp_buildDriver)

# end of file
