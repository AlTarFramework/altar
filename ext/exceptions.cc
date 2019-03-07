// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2019 parasim inc
// (c) 2010-2019 california institute of technology
// all rights reserved
//

#include <portinfo>
#include <Python.h>
#include <string>

#include "exceptions.h"

// the definition of the exception class
PyObject * altar::extensions::Error = 0;
const char * const altar::extensions::Error__name__ = "Error";


// end of file
