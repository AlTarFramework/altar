// -*- C++ -*-
//
// eric m. gurrola <eric.m.gurrola@jpl.nasa.gov>
//
// (c) 2019 california institute of technology / jet propulsion lab / nasa
// all rights reserved
//

#if !defined(altar_extensions_models_reverso_exceptions_h)
#define altar_extensions_models_reverso_exceptions_h


// place everything in my private namespace
namespace altar {
    namespace extensions {
        namespace models {
            namespace reverso {
                // base class for altar errors
                extern PyObject * Error;
                extern const char * const Error__name__;
            } // of namespace reverso
        } // of namespace models
    } // of namespace extensions
} // of namespace altar

#endif

// end of file
