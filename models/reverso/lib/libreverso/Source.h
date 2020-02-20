// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 2013-2020 parasim inc
// all rights reserved
//

// code guard
#if !defined(altar_models_reverso_Source_h)
#define altar_models_reverso_Source_h

// external
#include <vector>

// forward declarations
namespace altar::models::reverso {
    // forwards declarations
    class Source;

    // type aliases
    using source_t = Source;
}


// the reverso source
class altar::models::reverso::Source {
    // types
public:
    using size_type = std::size_t;

    // meta-methods
public:
    virtual ~Source();
    inline Source(double Qin, double G, double v, double mu, double drho, double g);

    // interface
public:
    inline void data(gsl_vector * data);
    inline void locations(gsl_matrix * locations);
    inline void layout(size_type HsIdx, size_type HdIdx,
                       size_type asIdx, size_type adIdx, size_type acIdx);

    void displacements(gsl_matrix_view * samples, gsl_matrix * predicted) const;
    void residuals(gsl_matrix * predicted) const;

    // implementation details
private:
    gsl_vector * _data;        // borrowed reference
    gsl_matrix * _locations;   // owned

    // the Poisson ratio
    double _Qin;
    double _G;
    double _v;
    double _mu;
    double _drho;
    double _g;

    // the layout of the various parameters within a sample
    size_type _HsIdx;
    size_type _HdIdx;
    size_type _asIdx;
    size_type _adIdx;
    size_type _acIdx;
};

// the implementations of the inline methods
#define altar_models_reverso_Source_icc
#include "Source.icc"
#undef altar_models_reverso_Source_icc

// code guard
#endif

// end of file
