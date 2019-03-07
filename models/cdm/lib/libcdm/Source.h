// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 2013-2019 parasim inc
// all rights reserved
//

// code guard
#if !defined(altar_models_cdm_Source_h)
#define altar_models_cdm_Source_h

// external
#include <vector>

// forward declarations
namespace altar {
    namespace models {
        namespace cdm {
            // forwards declarations
            class Source;

            // type aliases
            using source_t = Source;
        }
    }
}


// the cdm source
class altar::models::cdm::Source {
    // types
public:
    using size_type = std::size_t;
    using oids_type = std::vector<std::size_t>;

    // meta-methods
public:
    virtual ~Source();
    inline explicit Source(double nu);

    // interface
public:
    inline void data(gsl_vector * data);
    inline void locations(gsl_matrix * locations);
    inline void los(gsl_matrix * los);
    inline void oids(const oids_type & oids);
    inline void layout(size_type xIdx, size_type dIdx,
                       size_type openingIdx, size_type aXIdx, size_type omegaXIdx,
                       size_type offsetIdx);

    void displacements(gsl_matrix_view * samples, gsl_matrix * predicted) const;
    void residuals(gsl_matrix * predicted) const;

    // implementation details
private:
    gsl_vector * _data;        // borrowed reference
    gsl_matrix * _locations;   // owned
    gsl_matrix * _los;         // owned
    oids_type _oids;           // owned

    // the Poisson ratio
    double _nu;

    // the layout of the various parameters within a sample
    size_type _xIdx;
    size_type _yIdx;
    size_type _dIdx;
    size_type _openingIdx;
    size_type _aXIdx;
    size_type _aYIdx;
    size_type _aZIdx;
    size_type _omegaXIdx;
    size_type _omegaYIdx;
    size_type _omegaZIdx;
    size_type _offsetIdx;
};

// the implementations of the inline methods
#define altar_models_cdm_Source_icc
#include "Source.icc"
#undef altar_models_cdm_Source_icc

// code guard
#endif

// end of file
