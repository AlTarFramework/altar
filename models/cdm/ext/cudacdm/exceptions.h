// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2020 parasim inc
// all rights reserved
//

#if !defined(altar_extensions_models_cudacdm_exceptions_h)
#define altar_extensions_models_cudacdm_exceptions_h


// place everything in my private namespace
namespace altar {
    namespace extensions {
        namespace models {
            namespace cudacdm {
                // base class for altar errors
                extern PyObject * Error;
                extern const char * const Error__name__;
            } // of namespace cudacdm
        } // of namespace models
    } // of namespace extensions
} // of namespace altar

#endif

// end of file
