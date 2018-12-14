// -*- C++ -*-
//
// Lijun Zhu (ljzhu@caltech.edu)
//
// (c) 2013-2018 parasim inc
// (c) 2010-2018 california institute of technology
// all rights reserved
//

#if !defined(altar_extensions_utils_h)
#define altar_extensions_utils_h


// place everything in my private namespace
namespace altar {
    namespace extensions {

        // misc utilities
        namespace utils {
            extern const char * const matrix_condition__name__;
            extern const char * const matrix_condition__doc__;
            PyObject * matrix_condition(PyObject *, PyObject *);

        } // of namespace utils

    } // of namespace extensions
} // of namespace altar

#endif //altar_extensions_utils_h

// end of file
