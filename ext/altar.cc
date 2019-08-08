// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2019 parasim inc
// (c) 2010-2019 california institute of technology
// all rights reserved
//

// for the build system
#include <portinfo>
// external dependencies
#include <string>
#include <Python.h>

// the module method declarations
#include "exceptions.h"
#include "metadata.h"
#include "dbeta.h"


// put everything in my private namespace
namespace altar {
    namespace extensions {
        // the module method table
        PyMethodDef module_methods[] = {
            // module metadata
            // the copyright method
            { copyright__name__, copyright, METH_VARARGS, copyright__doc__ },
            // the license
            { license__name__, license, METH_VARARGS, license__doc__ },
            // the version
            { version__name__, version, METH_VARARGS, version__doc__ },

            // annealing schedule
            { cov__name__, cov, METH_VARARGS, cov__doc__},
            { dbeta_grid__name__, dbeta_grid, METH_VARARGS, dbeta_grid__doc__},
            { dbeta_gsl__name__, dbeta_gsl, METH_VARARGS, dbeta_gsl__doc__},

            // sentinel
            {0, 0, 0, 0}
        };

        // the module documentation string
        const char * const __doc__ = "sample module documentation string";

        // the module definition structure
        PyModuleDef module_definition = {
            // header
            PyModuleDef_HEAD_INIT,
            // the name of the module
            "altar",
            // the module documentation string
            __doc__,
            // size of the per-interpreter state of the module; -1 if this state is global
            -1,
            // the methods defined in this module
            module_methods
        };
    } // of namespace extensions
} // of namespace altar


// initialization function for the module
// *must* be called PyInit_altar
PyMODINIT_FUNC
PyInit_altar()
{
    // create the module
    PyObject * module = PyModule_Create(&altar::extensions::module_definition);
    // check whether module creation succeeded and raise an exception if not
    if (!module) {
        return 0;
    }
    // otherwise, we have an initialized module
    // return the newly created module
    return module;
}

// end of file
