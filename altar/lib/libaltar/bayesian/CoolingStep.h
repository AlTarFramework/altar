// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2020 parasim inc
// (c) 2010-2020 california institute of technology
// all rights reserved
//

// code guard
#if !defined(altar_bayesian_CoolingStep_h)
#define altar_bayesian_CoolingStep_h

// externals
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>

// place everything in the local namespace
namespace altar {
    namespace bayesian {

        // forward declarations
        class CoolingStep;

    } // of namespace bayesian
} // of namespace altar


// declaration
class altar::bayesian::CoolingStep
{
    // types
public:
    typedef gsl_vector vector_t;
    typedef gsl_matrix matrix_t;

    // interface
public:
    inline auto samples() const;
    inline auto parameters() const;

    inline auto beta() const;
    inline void beta(double value);

    inline auto theta() const;
    inline auto prior() const;
    inline auto data() const;
    inline auto posterior() const;
    inline auto sigma() const;

    // meta-methods
public:
    virtual ~CoolingStep();
    inline CoolingStep(size_t samples, size_t parameters, double beta=0.0);

    // data
private:
    const size_t _samples; // the number of samples
    const size_t _parameters; // the number of model parameters

    double _beta; // the current temperature
    matrix_t * const _theta; // the sample set, a (samples x parameters) matrix

    vector_t * const _prior; // the log likelihoods of the samples in the model prior
    vector_t * const _data; // the log likelihoods of the samples given the data
    vector_t * const _posterior; // the posterior log likelihood

    matrix_t * const _sigma; // the parameter covariance

    // disallow
private:
    CoolingStep(const CoolingStep &) = delete;
    const CoolingStep & operator=(const CoolingStep &) = delete;
};

// get the inline definitions
#define altar_bayesian_CoolingStep_icc
#include "CoolingStep.icc"
#undef altar_bayesian_CoolingStep_icc

# endif
// end of file
