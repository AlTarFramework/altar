// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2019 parasim inc
// all rights reserved
//

#if !defined(altar_extensions_models_cudacdm_source_h)
#define altar_extensions_models_cudacdm_source_h


// place everything in my private namespace
namespace altar {
    namespace extensions {
        namespace models {
            namespace cudacdm {
                // make a new source
                extern const char * const newSource__name__;
                extern const char * const newSource__doc__;
                PyObject * newSource(PyObject *, PyObject *);

                // attach the observations
                extern const char * const data__name__;
                extern const char * const data__doc__;
                PyObject * data(PyObject *, PyObject *);

                // attach the locations of the observation points
                extern const char * const locations__name__;
                extern const char * const locations__doc__;
                PyObject * locations(PyObject *, PyObject *);

                // attach the LOS vectors
                extern const char * const los__name__;
                extern const char * const los__doc__;
                PyObject * los(PyObject *, PyObject *);

                // the map of observations to their data set
                extern const char * const oid__name__;
                extern const char * const oid__doc__;
                PyObject * oid(PyObject *, PyObject *);

                // the structure of the parameter sets
                extern const char * const layout__name__;
                extern const char * const layout__doc__;
                PyObject * layout(PyObject *, PyObject *);

                // compute the residuals
                extern const char * const residuals__name__;
                extern const char * const residuals__doc__;
                PyObject * residuals(PyObject *, PyObject *);

            } // of namespace cudacdm
        } // of namespace models
    } // of namespace extensions
} // of namespace altar

#endif

// end of file
