# -*- cmake -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
# (c) 2003-2020 all rights reserved

# cmake setup
cmake_minimum_required(VERSION 3.12 FATAL_ERROR)
# policies
if (POLICY CMP0048)
  cmake_policy(SET CMP0048 NEW)
endif(POLICY CMP0048)
cmake_policy(SET CMP0060 NEW)
if (POLICY CMP0074)
  cmake_policy(SET CMP0074 NEW)
endif(POLICY CMP0074)
if (POLICY CMP0076)
  cmake_policy(SET CMP0076 NEW)
endif(POLICY CMP0076)

# options
option(WITH_CUDA "enable support for CUDA" OFF)

# adjust the include path
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/.cmake)
# get support
include(altar_init)

# ask git for the altar version
altar_getVersion()

# set up the project
project(ALTAR VERSION ${REPO_MAJOR}.${REPO_MINOR}.${REPO_MICRO} LANGUAGES CXX)

# packages
# gsl
find_package(GSL)
# mpi
find_package(MPI)
# python
set(PYTHON_COMPONENTS Interpreter Development)
if(GSL_FOUND)
    list(APPEND PYTHON_COMPONENTS NumPy)
endif()
find_package(Python3 REQUIRED COMPONENTS ${PYTHON_COMPONENTS})

# set up cmake
altar_cmakeInit()
# set up c++
altar_cxxInit()
# set up python
altar_pythonInit()

# initialize the variables that describe the staging directory layout
altar_stagingInit()
# initialize the variables that describe the install directory layout
altar_destinationInit()

# build the framework
add_subdirectory(altar)

# build the models
add_subdirectory(models/emhp)
add_subdirectory(models/gaussian)
add_subdirectory(models/mogi)
add_subdirectory(models/cdm)
add_subdirectory(models/linear)

# end of file
