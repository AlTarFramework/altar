// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2019 parasim inc
// all rights reserved
//

#include <portinfo>
#include <Python.h>

#include "metadata.h"
#include <altar/models/cdm/version.h>

// version
const char * const altar::extensions::models::cdm::version__name__ = "version";
const char * const altar::extensions::models::cdm::version__doc__ = "the module version string";
PyObject *
altar::extensions::models::cdm::
version(PyObject *, PyObject *)
{
    return Py_BuildValue("s", altar::models::cdm::version());
}


// end of file
