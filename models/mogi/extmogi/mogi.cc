// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2018 parasim inc
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


// put everything in my private namespace
namespace altar {
    namespace extensions {
        namespace models {
            namespace mogi {
                // the module method table
                PyMethodDef module_methods[] = {
                    // module metadata
                    // the version
                    { version__name__, version, METH_VARARGS, version__doc__ },

                    // sentinel
                    {0, 0, 0, 0}
                };

                // the module documentation string
                const char * const __doc__ = "the mogi extension module";

                // the module definition structure
                PyModuleDef module_definition = {
                    // header
                    PyModuleDef_HEAD_INIT,
                    // the name of the module
                    "mogi",
                    // the module documentation string
                    __doc__,
                    // size of the per-interpreter state of the module; -1 if this state is global
                    -1,
                    // the methods defined in this module
                    module_methods
                };
            } // of namespace mogi
        } // of namespace models
    } // of namespace extensions
} // of namespace altar


// initialization function for the module
// *must* be called PyInit_altar
PyMODINIT_FUNC
PyInit_mogi()
{
    // create the module
    PyObject * module = PyModule_Create(&altar::extensions::models::mogi::module_definition);
    // check whether module creation succeeded and raise an exception if not
    if (!module) {
        return 0;
    }
    // otherwise, we have an initialized module
    // return the newly created module
    return module;
}

// end of file
