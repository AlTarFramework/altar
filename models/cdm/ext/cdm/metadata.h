// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2020 parasim inc
// all rights reserved
//

#if !defined(altar_extensions_models_cdm_metadata_h)
#define altar_extensions_models_cdm_metadata_h


// place everything in my private namespace
namespace altar::extensions::models::cdm {
    // version
    extern const char * const version__name__;
    extern const char * const version__doc__;
    PyObject * version(PyObject *, PyObject *);
}

#endif

// end of file
