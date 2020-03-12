# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved

# build the reverso package
function(altar_reverso_buildPackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY reverso
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    reverso/meta.py.in reverso/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/reverso
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(altar_reverso_buildPackage)


# buld the reverso libraries
function(altar_reverso_buildLibrary)
  # the libreverso target
  add_library(libreverso SHARED)
  # adjust the name
  set_target_properties(
    libreverso PROPERTIES
    LIBRARY_OUTPUT_NAME reverso
    )
  # set the include directories
  target_include_directories(
    libreverso PRIVATE
    ${CMAKE_INSTALL_PREFIX}/include
    ${GSL_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS}
    )
  # set the link directories
  target_link_directories(
    libreverso PRIVATE
    ${CMAKE_INSTALL_PREFIX}/lib
    )
  # add the dependencies
  target_link_libraries(
    libreverso PRIVATE
    ${GSL_LIBRARIES} journal
    )
  # add the sources
  target_sources(
    libreverso PRIVATE
    lib/libreverso/reverso.cc
    lib/libreverso/Source.cc
    )

  # copy the reverso headers; note the trickery with the terminating slash in the source
  # directory that lets us place the files in the correct destination
  file(
    COPY lib/libreverso/
    DESTINATION ${CMAKE_INSTALL_PREFIX}/${ALTAR_DEST_INCLUDE}/altar/models/reverso
    FILES_MATCHING PATTERN *.h PATTERN *.icc
    )

  # install the library
  install(
    TARGETS libreverso
    LIBRARY DESTINATION lib
    )

  # all done
endfunction(altar_reverso_buildLibrary)


# build the reverso extension module
function(altar_reverso_buildModule)
  # reverso
  Python3_add_library(reversomodule MODULE)
  # adjust the name to match what python expects
  set_target_properties(
    reversomodule PROPERTIES
    LIBRARY_OUTPUT_NAME reverso
    SUFFIX ${PYTHON3_SUFFIX}
    )
  # set the include directories
  target_include_directories(
    reversomodule PRIVATE
    ${CMAKE_INSTALL_PREFIX}/include
    ${GSL_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS}
    )
  # set the link directories
  target_link_directories(
    reversomodule PRIVATE
    ${CMAKE_INSTALL_PREFIX}/lib
    )
  # set the libraries to link against
  target_link_libraries(reversomodule PUBLIC libreverso libaltar journal)
  # add the sources
  target_sources(reversomodule PRIVATE
    ext/reverso/reverso.cc
    ext/reverso/exceptions.cc
    ext/reverso/source.cc
    )

  # install the capsule
  install(
    FILES ext/reverso/capsules.h
    DESTINATION ${ALTAR_DEST_INCLUDE}/altar/models/reverso
    )

  # install the reverso extension
  install(
    TARGETS reversomodule
    LIBRARY
    DESTINATION ${CMAKE_INSTALL_PREFIX}/packages/altar/models/reverso/ext
    )
endfunction(altar_reverso_buildModule)


# the scripts
function(altar_reverso_buildDriver)
  # install the scripts
  install(
    PROGRAMS bin/reverso
    DESTINATION bin
    )
  # all done
endfunction(altar_reverso_buildDriver)

# end of file
