# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved

# build the altar package
function(altar_buildPackage)
  # install the sources straight from the source directory
  install(
    DIRECTORY altar
    DESTINATION ${ALTAR_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # build the package meta-data
  configure_file(
    altar/meta.py.in altar/meta.py
    @ONLY
    )
  # install the generated package meta-data file
  install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/altar
    DESTINATION ${ALTAR_DEST_PACKAGES}
    FILES_MATCHING PATTERN *.py
    )
  # all done
endfunction(altar_buildPackage)


# buld the altar libraries
function(altar_buildLibrary)
  # the libaltar target
  add_library(libaltar SHARED)
  # adjust the name
  set_target_properties(
    libaltar PROPERTIES
    LIBRARY_OUTPUT_NAME altar
    )

  # set the include directories
  target_include_directories(
    libaltar PRIVATE
    ${CMAKE_INSTALL_PREFIX}/include
    ${GSL_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS}
    )
  # add the dependencies
  target_link_libraries(
    libaltar PRIVATE
    ${GSL_LIBRARIES}
    )
  # add the sources
  target_sources(
    libaltar PRIVATE
    lib/libaltar/bayesian/CoolingStep.cc
    lib/libaltar/bayesian/COV.cc
    )

  # copy the altar headers; note the trickery with the terminating slash in the source
  # directory that let's us place the files in the correct destination
  file(
    COPY lib/libaltar/
    DESTINATION ${CMAKE_INSTALL_PREFIX}/${ALTAR_DEST_INCLUDE}/altar
    FILES_MATCHING PATTERN *.h PATTERN *.icc
    )

  # install the library
  install(
    TARGETS libaltar
    LIBRARY DESTINATION lib
    )

  # all done
endfunction(altar_buildLibrary)


# build the altar extension module
function(altar_buildModule)
  # altar
  Python3_add_library(altarmodule MODULE)
  # adjust the name to match what python expects
  set_target_properties(
    altarmodule PROPERTIES
    LIBRARY_OUTPUT_NAME altar
    SUFFIX ${PYTHON3_SUFFIX}
    )
  # set the include directories
  target_include_directories(
    altarmodule PRIVATE
    ${CMAKE_INSTALL_PREFIX}/include
    ${GSL_INCLUDE_DIRS} ${Python3_NumPy_INCLUDE_DIRS}
    )
  # set  the link directories
  target_link_directories(
    altarmodule PRIVATE
    ${CMAKE_INSTALL_PREFIX}/lib
    )
  # set the libraries to link against
  target_link_libraries(altarmodule PRIVATE libaltar journal)
  # add the sources
  target_sources(altarmodule PRIVATE
    ext/altar.cc
    ext/metadata.cc
    ext/exceptions.cc
    ext/dbeta.cc
    )

  # install the altar extension
  install(
    TARGETS altarmodule
    LIBRARY
    DESTINATION ${CMAKE_INSTALL_PREFIX}/packages/altar/ext
    )
endfunction(altar_buildModule)


# the scripts
function(altar_buildDriver)
  # install the scripts
  install(
    PROGRAMS bin/altar
    DESTINATION bin
    )
  # all done
endfunction(altar_buildDriver)

# end of file
