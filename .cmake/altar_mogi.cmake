# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved

# build the mogi package
function(altar_mogi_buildPackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY mogi
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    mogi/meta.py.in mogi/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/mogi
    DESTINATION ${ALTAR_DEST_PACKAGES}/altar/models
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(altar_mogi_buildPackage)


# buld the mogi libraries
function(altar_mogi_buildLibrary)
  # the libmogi target
  add_library(libmogi SHARED)
  # adjust the name
  set_target_properties(
    libmogi PROPERTIES
    LIBRARY_OUTPUT_NAME mogi
    )
  # set the include directories
  target_include_directories(
    libmogi PRIVATE
    ${CMAKE_INSTALL_PREFIX}/include
    ${GSL_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS}
    )
  # set the link directories
  target_link_directories(
    libmogi PRIVATE
    ${CMAKE_INSTALL_PREFIX}/lib
    )
  # add the dependencies
  target_link_libraries(
    libmogi PRIVATE
    ${GSL_LIBRARIES} journal
    )
  # add the sources
  target_sources(
    libmogi PRIVATE
    lib/libmogi/version.cc
    lib/libmogi/Source.cc
    )

  # copy the mogi headers; note the trickery with the terminating slash in the source
  # directory that let's us place the files in the correct destination
  file(
    COPY lib/libmogi/
    DESTINATION ${CMAKE_INSTALL_PREFIX}/${ALTAR_DEST_INCLUDE}/altar/models/mogi
    FILES_MATCHING PATTERN *.h PATTERN *.icc
    )

  # install the library
  install(
    TARGETS libmogi
    LIBRARY DESTINATION lib
    )

  # all done
endfunction(altar_mogi_buildLibrary)


# build the mogi extension module
function(altar_mogi_buildModule)
  # mogi
  Python3_add_library(mogimodule MODULE)
  # adjust the name to match what python expects
  set_target_properties(
    mogimodule PROPERTIES
    LIBRARY_OUTPUT_NAME mogi
    SUFFIX ${PYTHON3_SUFFIX}
    )
  # set the include directories
  target_include_directories(
    mogimodule PRIVATE
    ${CMAKE_INSTALL_PREFIX}/include
    ${GSL_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS}
    )
  # set the link directories
  target_link_directories(
    mogimodule PRIVATE
    ${CMAKE_INSTALL_PREFIX}/lib
    )
  # set the libraries to link against
  target_link_libraries(mogimodule PUBLIC libmogi libaltar journal)
  # add the sources
  target_sources(mogimodule PRIVATE
    ext/mogi/mogi.cc
    ext/mogi/metadata.cc
    ext/mogi/exceptions.cc
    ext/mogi/source.cc
    )

  # install the capsule
  install(
    FILES ext/mogi/capsules.h
    DESTINATION ${ALTAR_DEST_INCLUDE}/altar/models/mogi
    )

  # install the mogi extension
  install(
    TARGETS mogimodule
    LIBRARY
    DESTINATION ${CMAKE_INSTALL_PREFIX}/packages/altar/models/mogi/ext
    )
endfunction(altar_mogi_buildModule)


# the scripts
function(altar_mogi_buildDriver)
  # install the scripts
  install(
    PROGRAMS bin/mogi
    DESTINATION bin
    )
  # all done
endfunction(altar_mogi_buildDriver)

# end of file
