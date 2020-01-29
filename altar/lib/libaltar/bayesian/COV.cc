// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2020 parasim inc
// (c) 2010-2020 california institute of technology
// all rights reserved
//


// for the build system
#include <portinfo>

// for debugging
# include <cassert>

// externals
#include <cmath>
#include <iostream>
#include <iomanip>
#include <gsl/gsl_sys.h>
#include <gsl/gsl_min.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_roots.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_histogram.h>
#include <gsl/gsl_statistics.h>
#include <gsl/gsl_sort_vector.h>

#include <pyre/journal.h>

// get my declarations
#include "COV.h"
// and my dependencies
#include "CoolingStep.h"

// workhorses
namespace cov {
    // the COV calculator
    static double cov(double, void *);
    // and its parameter structure
    struct args {
        double dbeta; // the current proposal for dbeta
        double cov; // the current value of COV
        double metric; // the latest value of our objective function

        // inputs from the higher levels
        gsl_vector * w; // the vector of weights
        gsl_vector * llk; // the vector of data log-likelihoods
        double llkMedian; // the median value of the log-likelihoods
        double target; // the COV value we are aiming for; should be 1
    };
}

// interface
// calculate the beta increment with gsl minimizer
double
altar::bayesian::COV::
dbeta_brent(vector_t *llk, double llkMedian, vector_t *w)
{
    // build my debugging channel
    pyre::journal::debug_t debug("altar.beta");

    // turn off the err_handler, return previous handler

    // MGA 20190925:
    //   i'm not sure i like shutting down the GSL error reporting mechanism; it's true that
    //   the previous behavior, i.e. letting the GSL errors surface all the way up to the user,
    //   was also bad, but it was meant to be a reminder that something sensible has to happen
    //   while observing the behavior of the solver with real models. we need to think this
    //   through and put together a mechanism for handling and propagating errors through to
    //   the python layer where they can be handled in a user friendly way
    //
    gsl_error_handler_t * gsl_hdl = gsl_set_error_handler_off();

    // consistency checks
    assert(_betaMin == 0);
    assert(_betaMax == 1);

    // the beta search region
    double beta_low = 0;
    double beta_high = _betaMax - _beta;
    double beta_guess = _betaMin + 5.0e-5;

    assert(beta_high >= beta_low);
    assert(beta_high >= beta_guess);
    assert(beta_guess >= beta_low);

    // allocate space for the parameters
    cov::args covargs;
    // attach the two vectors
    covargs.w = w;
    covargs.llk = llk;
    // store our initial guess
    covargs.dbeta = beta_guess;
    // initialize the COV target
    covargs.target = _target;
    // initialize the median of the log-likelihoods
    covargs.llkMedian = llkMedian;

    // search bounds and initial guess
    double f_beta_high = cov::cov(beta_high, &covargs);

    // check whether we can skip straight to beta = 1
    if (covargs.cov < _target || std::abs(covargs.cov-_target) < _tolerance) {
        debug
            << pyre::journal::at(__HERE__)
            << " ** skipping to beta = " << _betaMax << " **"
            << pyre::journal::endl;
        // save my state
        _beta = _betaMax;
        _cov = covargs.cov;
        // all done
        return beta_high;
    }

    double f_beta_low = cov::cov(beta_low, &covargs);
    // do this last so our first printout reflects the values at out guess
    double f_beta_guess = cov::cov(beta_guess, &covargs);

    // lie to the minimizer, if necessary
    // if (f_beta_low < f_beta_guess) f_beta_low = 1.01 * f_beta_guess;
    // if (f_beta_high < f_beta_guess) f_beta_high = 1.01 * f_beta_guess;

    // instantiate the minimizer
    gsl_min_fminimizer * minimizer = gsl_min_fminimizer_alloc(gsl_min_fminimizer_brent);
    // set up the minimizer call back
    gsl_function F;
    F.function = cov::cov;
    F.params = &covargs;
    // prime it
    gsl_min_fminimizer_set_with_values(
                                       minimizer, &F,
                                       beta_guess, f_beta_guess,
                                       beta_low, f_beta_low,
                                       beta_high, f_beta_high);
    // duplicate the catmip output, for now
    size_t iter = 0;
    if (debug) {
        std::cout
            << "    "
            << "Calculating dbeta using "
            << gsl_min_fminimizer_name(minimizer) << " method" << std::endl
            << "      median data llk: "
            << std::fixed << std::setw(11) << std::setprecision(4) << llkMedian << std::endl
            << "      target: " << _target << std::endl
            << "      tolerance: " << _tolerance << std::endl
            << "      max iterations: " << _maxIterations
            << std::endl;
        std::cout
            << "     "
            << std::setw(6) << " iter"
            " [" << std::setw(11) << "lower"
            << ", " << std::setw(11) << "upper" << "]"
            << " " << std::setw(11) << "dbeta  "
            << " " << std::setw(11) << "cov  "
            << " " << std::setw(11) << "err  "
            << " " << std::setw(11) << "f(dbeta)"
            << std::endl;
        std::cout.setf(std::ios::scientific, std::ios::floatfield);
        std::cout
            << "     "
            << std::setw(5) << iter
            << " [" << std::setw(11) << std::setprecision(4) << beta_low
            << ", " << std::setw(11) << beta_high << "] "
            << " " << std::setw(11) << covargs.dbeta
            << " " << std::setw(11) << covargs.cov
            << " " << std::setw(11) << covargs.cov - _target
            << " " << std::setw(11) << covargs.metric
            << std::endl;
    }

    // the GSL flag
    int status;
    // iterate, looking for the minimum
    do {
        iter++;
        status = gsl_min_fminimizer_iterate(minimizer);
        beta_low = gsl_min_fminimizer_x_lower(minimizer);
        beta_high = gsl_min_fminimizer_x_upper(minimizer);
        status = gsl_root_test_residual(covargs.cov-_target,  _tolerance);

        // print the result
        if (debug) {
            std::cout
                << "     "
                << std::setw(5) << iter
                << " [" << std::setw(11) << std::setprecision(4) << beta_low
                << ", " << std::setw(11) << beta_high << "] "
                << " " << std::setw(11) << covargs.dbeta
                << " " << std::setw(11) << covargs.cov
                << " " << std::setw(11) << covargs.cov - _target
                << " " << std::setw(11) << covargs.metric;

            if (status == GSL_SUCCESS) {
                std::cout << " (Converged)";
            }
            std::cout << std::endl;
        }

    } while (status == GSL_CONTINUE && iter < _maxIterations);

    // get the best guess at the minimum
    double dbeta = gsl_min_fminimizer_x_minimum(minimizer);
    // make sure that we are left with the COV and weights evaluated for this guess
    cov::cov(dbeta, &covargs);

    // free the minimizer
    gsl_min_fminimizer_free(minimizer);
    // restore previous gsl_error_handler
    gsl_set_error_handler(gsl_hdl);

    // adjust my state
    _cov = covargs.cov;
    _beta += dbeta;
    // return the beta update
    return dbeta;
}

// calculate the new annealing temperature by iterative grid-based searching
double
altar::bayesian::COV::
dbeta_grid(vector_t *llk, double llkMedian, vector_t *w)
{
    // build my debugging channel
    pyre::journal::debug_t debug("altar.beta");

    // consistency checks
    assert(_betaMin == 0);
    assert(_betaMax == 1);

    // the beta search region
    double beta_low = 0;
    double beta_high = _betaMax - _beta;
    double beta_guess = _betaMin + 5.0e-5;

    assert(beta_high >= beta_low);
    assert(beta_high >= beta_guess);
    assert(beta_guess >= beta_low);

    // allocate space for the parameters
    cov::args covargs;
    // attach the two vectors
    covargs.w = w;
    covargs.llk = llk;
    // store our initial guess
    covargs.dbeta = beta_guess;
    // initialize the COV target
    covargs.target = _target;
    // initialize the median of the log-likelihoods
    covargs.llkMedian = llkMedian;

    // search bounds and initial guess
    double f_beta_high = cov::cov(beta_high, &covargs);

    // check whether we can skip straight to beta = 1
    if (covargs.cov < _target || std::abs(covargs.cov-_target) < _tolerance) {
        debug
            << pyre::journal::at(__HERE__)
            << " ** skipping to beta = " << _betaMax << " **"
            << pyre::journal::endl;
        // save my state
        _beta = _betaMax;
        _cov = covargs.cov;
        // all done
        return beta_high;
    }

    double f_beta_low = cov::cov(beta_low, &covargs);
    // do this last so our first printout reflects the values at out guess
    double f_beta_guess = cov::cov(beta_guess, &covargs);

    // iterative grid searching
    //double beta_grid_tolerance=1.E-6;
    const int Nbeta=10;
    int nbeta = 0;
    double dbeta, beta_step;
    int Nloop = 0;
    if (debug) std::cout<<"dbeta minimization based on iterative grid searching:"<<std::endl;
    bool Qfind = false;
    do
    {
        ++Nloop;
        beta_step = (beta_high-beta_low)/Nbeta;
        int count=0;
        for (beta_guess=beta_low, nbeta=0; nbeta<=Nbeta; beta_guess+=beta_step, ++nbeta)
        {
            f_beta_guess = cov::cov(beta_guess, &covargs);
            if (std::abs(covargs.cov-_target) < _tolerance)
            {
                Qfind = true;
                break;
            }
            if (covargs.cov >= _target)
            {
               if (nbeta==0) Qfind = true;
               break;
            }
        }
        if (nbeta>Nbeta) beta_guess -= beta_step;
        if (debug){
            std::cout
                <<"      dbeta_low: "<<std::setw(11)<<std::setprecision(8)<<beta_low
                <<"      dbeta_high: "<<std::setw(11)<<beta_high
                <<"      dbeta_guess: "<<std::setw(11)<<beta_guess
                <<"      cov: "<<std::setw(15)<<covargs.cov
                << std::endl;
        }
        beta_high = beta_guess;
        beta_low = beta_guess-beta_step;
    }
    while (Nloop<=Nbeta && !Qfind);

    // assign dbeta
    dbeta = beta_guess;

    // make sure that we are left with the COV and weights evaluated for this guess
    cov::cov(dbeta, &covargs);

    // adjust my state
    _cov = covargs.cov;
    _beta += dbeta;
    // return the beta update
    return dbeta;
}

// meta-methods
altar::bayesian::COV::
~COV()
{}


// compute the coefficient of variation (COV)
double cov::cov(double dbeta, void * parameters)
{
    // get my auxiliary parameters
    args & p = *static_cast<cov::args *>(parameters);
    // store dbeta
    p.dbeta = dbeta;

    // initialize {w}
    for (size_t i = 0; i < p.w->size; i++) {
        gsl_vector_set(p.w, i, std::exp(dbeta * (gsl_vector_get(p.llk, i)  - p.llkMedian)));
    }
    // normalize
    double wsum = p.w->size * gsl_stats_mean(p.w->data, p.w->stride, p.w->size);
    gsl_vector_scale(p.w, 1/wsum);

    // compute the COV
    double mean = gsl_stats_mean(p.w->data, p.w->stride, p.w->size);
    double sdev = gsl_stats_sd_m(p.w->data, p.w->stride, p.w->size, mean);
    double cov = sdev / mean;

    // if the COV is not well defined
    if (gsl_isinf(cov) || gsl_isnan(cov)) {
        // set our metric to some big value
        p.metric = 1e100;
        p.cov = 1e100;
    } else {
        // otherwise
        p.metric = gsl_pow_2(cov - p.target);
        p.cov =cov;
    }

    // and return
    return p.metric;
}

// end of file
