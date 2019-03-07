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
#include <altar/models/cudamogi/version.h>

// version
const char * const
altar::extensions::models::cudamogi::version__name__ = "version";

const char * const
altar::extensions::models::cudamogi::version__doc__ = "the module version string";

PyObject *
altar::extensions::models::cudamogi::
version(PyObject *, PyObject *)
{
    return Py_BuildValue("s", altar::models::cudamogi::version());
}


// end of file
