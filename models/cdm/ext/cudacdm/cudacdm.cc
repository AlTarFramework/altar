// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2020 parasim inc
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
#include "source.h"


// put everything in my private namespace
namespace altar {
    namespace extensions {
        namespace models {
            namespace cudacdm {
                // the module method table
                extern PyMethodDef module_methods[];
                extern PyModuleDef module_definition;
            } // of namespace cudacdm
        } // of namespace models
    } // of namespace extensions
} // of namespace altar

PyMethodDef
altar::extensions::models::cudacdm::
module_methods[] = {
    // module metadata
    // the version
    { version__name__, version, METH_VARARGS, version__doc__ },

    // source methods
    // constructor
    { newSource__name__, newSource, METH_VARARGS, newSource__doc__ },
    // user supplied information
    { data__name__, data, METH_VARARGS, data__doc__ },
    { locations__name__, locations, METH_VARARGS, locations__doc__ },
    { los__name__, los, METH_VARARGS, los__doc__ },
    { oid__name__, oid, METH_VARARGS, oid__doc__ },
    { layout__name__, layout, METH_VARARGS, layout__doc__ },
    // and the residuals
    { residuals__name__, residuals, METH_VARARGS, residuals__doc__ },

    // sentinel
    {0, 0, 0, 0}
};

// the module definition structure
PyModuleDef
altar::extensions::models::cudacdm::
module_definition = {
    // header
    PyModuleDef_HEAD_INIT,
    // the name of the module
    "cudacdm",
    // the module documentation string
    "the cdm extension module with support for CUDA",
    // size of the per-interpreter state of the module; -1 if this state is global
    -1,
    // the methods defined in this module
    module_methods
};

// initialization function for the module
// *must* be called PyInit_altar
PyMODINIT_FUNC
PyInit_cudacdm()
{
    // create the module
    PyObject * module = PyModule_Create(&altar::extensions::models::cudacdm::module_definition);
    // check whether module creation succeeded
    if (!module) {
        // and raise an exception if not
        return 0;
    }
    // otherwise, we have an initialized module
    // return the newly created module
    return module;
}

// end of file
