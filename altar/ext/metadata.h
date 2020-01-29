// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2020 parasim inc
// (c) 2010-2020 california institute of technology
// all rights reserved
//

#if !defined(altar_extensions_metadata_h)
#define altar_extensions_metadata_h


// place everything in my private namespace
namespace altar {
    namespace extensions {
        // copyright note
        extern const char * const copyright__name__;
        extern const char * const copyright__doc__;
        PyObject * copyright(PyObject *, PyObject *);

        // license
        extern const char * const license__name__;
        extern const char * const license__doc__;
        PyObject * license(PyObject *, PyObject *);

        // version
        extern const char * const version__name__;
        extern const char * const version__doc__;
        PyObject * version(PyObject *, PyObject *);

    } // of namespace extensions
} // of namespace altar

#endif

// end of file
