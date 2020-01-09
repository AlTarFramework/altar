// -*- C++ -*-
//
// eric m. gurrola
//
// (c) 2013-2019 california institute of technology / jet propulsion lab, nasa
// all rights reserved
//

#if !defined(altar_extensions_models_reverso_metadata_h)
#define altar_extensions_models_reverso_metadata_h


// place everything in my private namespace
namespace altar {
    namespace extensions {
        namespace models {
            namespace reverso {
                // version
                extern const char * const version__name__;
                extern const char * const version__doc__;
                PyObject * version(PyObject *, PyObject *);
            } // of namespace reverso
        } // of namespace models
    } // of namespace extensions
} // of namespace altar

#endif

// end of file
