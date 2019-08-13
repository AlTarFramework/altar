// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2019 parasim inc
// (c) 2010-2019 california institute of technology
// all rights reserved
//

// code guard
#if !defined(altar_bayesian_COV_h)
#define altar_bayesian_COV_h

// externals
#include <gsl/gsl_rng.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>

// place everything in the local namespace
namespace altar {
    namespace bayesian {

        // forward declarations
        class COV;
        class CoolingStep;

    } // of namespace bayesian
} // of namespace altar

// declaration
class altar::bayesian::COV
{
    // types
public:
    typedef CoolingStep state_t;

    typedef gsl_rng rng_t;
    typedef gsl_vector vector_t;
    typedef gsl_matrix matrix_t;

    // accessors
public:
    inline auto cov() const;
    inline auto beta() const;

    // interface
public:
    virtual double dbeta_brent(vector_t * llk, double llkMedian, vector_t * w);
    virtual double dbeta_grid(vector_t * llk, double llkMedian, vector_t * w);

    // meta-methods
public:
    virtual ~COV();
    inline COV(
               rng_t * rng,
               double tolerance=.001, size_t maxIterations=1000, double target=1.0
               );

    // data
private:
    const double _betaMin;
    const double _betaMax;

    rng_t * _rng;
    double _tolerance;
    size_t _maxIterations;
    double  _target;
    double _beta, _cov;

    // disallow
private:
    COV(const COV &) = delete;
    const COV & operator=(const COV &) = delete;
};

// get the inline definitions
#define altar_bayesian_COV_icc
#include "COV.icc"
#undef altar_bayesian_COV_icc

# endif
// end of file
