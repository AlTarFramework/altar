// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2019 parasim inc
// all rights reserved
//

#if !defined(altar_extensions_models_cudacdm_metadata_h)
#define altar_extensions_models_cudacdm_metadata_h


// place everything in my private namespace
namespace altar {
    namespace extensions {
        namespace models {
            namespace cudacdm {
                // version
                extern const char * const version__name__;
                extern const char * const version__doc__;
                PyObject * version(PyObject *, PyObject *);
            } // of namespace cudacdm
        } // of namespace models
    } // of namespace extensions
} // of namespace altar

#endif

// end of file
