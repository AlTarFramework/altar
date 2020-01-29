# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved

# build the cdm package
function(altar_cdm_buildPackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY cdm
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    cdm/meta.py.in cdm/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/cdm
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(altar_cdm_buildPackage)


# buld the cdm libraries
function(altar_cdm_buildLibrary)
  # the libcdm target
  add_library(libcdm SHARED)
  # adjust the name
  set_target_properties(
    libcdm PROPERTIES
    LIBRARY_OUTPUT_NAME cdm
    )
  # set the include directories
  target_include_directories(
    libcdm PRIVATE
    ${CMAKE_INSTALL_PREFIX}/include
    ${GSL_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS}
    )
  # set the link directories
  target_link_directories(
    libcdm PRIVATE
    ${CMAKE_INSTALL_PREFIX}/lib
    )
  # add the dependencies
  target_link_libraries(
    libcdm PRIVATE
    ${GSL_LIBRARIES} journal
    )
  # add the sources
  target_sources(
    libcdm PRIVATE
    lib/libcdm/cdm.cc
    lib/libcdm/version.cc
    lib/libcdm/Source.cc
    )

  # copy the cdm headers; note the trickery with the terminating slash in the source
  # directory that let's us place the files in the correct destination
  file(
    COPY lib/libcdm/
    DESTINATION ${CMAKE_INSTALL_PREFIX}/${ALTAR_DEST_INCLUDE}/altar/models/cdm
    FILES_MATCHING PATTERN *.h PATTERN *.icc
    )

  # install the library
  install(
    TARGETS libcdm
    LIBRARY DESTINATION lib
    )

  # all done
endfunction(altar_cdm_buildLibrary)


# build the cdm extension module
function(altar_cdm_buildModule)
  # cdm
  Python3_add_library(cdmmodule MODULE)
  # adjust the name to match what python expects
  set_target_properties(
    cdmmodule PROPERTIES
    LIBRARY_OUTPUT_NAME cdm
    SUFFIX ${PYTHON3_SUFFIX}
    )
  # set the include directories
  target_include_directories(
    cdmmodule PRIVATE
    ${CMAKE_INSTALL_PREFIX}/include
    ${GSL_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS}
    )
  # set the link directories
  target_link_directories(
    cdmmodule PRIVATE
    ${CMAKE_INSTALL_PREFIX}/lib
    )
  # set the libraries to link against
  target_link_libraries(cdmmodule PUBLIC libcdm libaltar journal)
  # add the sources
  target_sources(cdmmodule PRIVATE
    ext/cdm/cdm.cc
    ext/cdm/metadata.cc
    ext/cdm/exceptions.cc
    ext/cdm/source.cc
    )

  # install the capsule
  install(
    FILES ext/cdm/capsules.h
    DESTINATION ${ALTAR_DEST_INCLUDE}/altar/models/cdm
    )

  # install the cdm extension
  install(
    TARGETS cdmmodule
    LIBRARY
    DESTINATION ${CMAKE_INSTALL_PREFIX}/packages/altar/models/cdm/ext
    )
endfunction(altar_cdm_buildModule)


# the scripts
function(altar_cdm_buildDriver)
  # install the scripts
  install(
    PROGRAMS bin/cdm
    DESTINATION bin
    )
  # all done
endfunction(altar_cdm_buildDriver)

# end of file
