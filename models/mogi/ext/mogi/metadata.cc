// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2020 parasim inc
// all rights reserved
//

#include <portinfo>
#include <Python.h>

#include "metadata.h"
#include <altar/models/mogi/version.h>

// version
const char * const altar::extensions::models::mogi::version__name__ = "version";
const char * const altar::extensions::models::mogi::version__doc__ = "the module version string";
PyObject *
altar::extensions::models::mogi::
version(PyObject *, PyObject *)
{
    return Py_BuildValue("s", altar::models::mogi::version());
}


// end of file
