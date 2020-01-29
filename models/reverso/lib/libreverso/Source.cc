// -*- C++ -*-
//
// eric m. gurrola <eric.m.gurrola@jpl.nasa.gov>
// california institute of technology * jet propulsion lab * nasa
// (c) 2013-2020 parasim inc
// all rights reserved
//

// configuration
#include <portinfo>
// external
#include <cmath>
#include <pyre/journal.h>
#include <gsl/gsl_matrix.h>

// support
#include "reverso.h"

// my declarations
#include "Source.h"

// meta-methods
// destructor
altar::models::reverso::Source::
~Source() {
    // make a channel
    pyre::journal::debug_t channel("reverso.source");

    // sign on
    channel
        << pyre::journal::at(__HERE__)
        << "deleting source " << this
        << pyre::journal::endl;

    // if we were handed a matrix of the locations of the observation points
    if (_locations) {
        // release it
        gsl_matrix_free(_locations);
        // tell me
        channel
            << pyre::journal::at(__HERE__)
            << "  released {_locations} matrix at" << _locations
            << pyre::journal::endl;
    }

    // if we were handed a matrix of line of sight vectors
    if (_los) {
        // release it
        gsl_matrix_free(_los);
        // tell me
        channel
            << pyre::journal::at(__HERE__)
            << "  released {_los} matrix at" << _los
            << pyre::journal::endl;
    }

    // all done
    channel
        << pyre::journal::at(__HERE__)
        << "done deleting source " << this
        << pyre::journal::endl;
}


// interface
void
altar::models::reverso::Source::
displacements(gsl_matrix_view * samples, gsl_matrix * predicted) const {
    // pull the number of samples and parameters from the shape of the {sample} matrix
    auto nSamples = samples->matrix.size1;
    auto nParameters = samples->matrix.size2;

    // clean up the resulting matrix
    gsl_matrix_set_zero(predicted);

    // go through all the samples
    for (auto sample=0; sample<nSamples; ++sample) {
        // unpack the parameters
        // x, y position of the center of the connecting tube = space origin (z0Src=0)
        auto x0Src = gsl_matrix_get(&samples->matrix, sample, _x0Idx);
        auto y0Src = gsl_matrix_get(&samples->matrix, sample, _y0Idx);
        // time origin
        auto t0Src = gsl_matrix_get(&samples->matrix, sample, _t0Idx);
        // depth and radius of the shallow reservoir
        auto hsSrc = gsl_matrix_get(&samples->matrix, sample, _hsIdx);
        auto asSrc = gsl_matrix_get(&samples->matrix, sample, _asIdx);
        // depth and radius of the deep reservoir
        auto hdSrc = gsl_matrix_get(&samples->matrix, sample, _hdIdx);
        auto adSrc = gsl_matrix_get(&samples->matrix, sample, _adIdx);
        // radius of the connecting tube between the two reservoirs
        auto acSrc = gsl_matrix_get(&samples->matrix, sample, _acIdx);
        // base magma inflow rate from below the deep reservoir
        auto qSrc  = gsl_matrix_get(&samples->matrix, sample, _qIdx);

        //compute the displacements
        reverso(sample, _locations, _los,
                x0Src, y0Src, t0Src,
                hsSrc, asSrc,
                hdSrc, adSrc,
                acSrc, qSrc,
                _nu, _mu,
        // apply the location specific projection to LOS vector and dataset shift
        for (auto loc=0; loc<_locations->size1; ++loc) {
            // get the current value
            auto u = gsl_matrix_get(predicted, sample, loc);
            // find the shift that corresponds to this observation
            auto shift = gsl_matrix_get(&samples->matrix, sample, _offsetIdx+_oids[loc]);
            // and apply it to the projected displacement
            u -= shift;
            // save
            gsl_matrix_set(predicted, sample, loc, u);
        }
    }

    // all done
    return;
}


void
altar::models::reverso::Source::
residuals(gsl_matrix * predicted) const {
    // make a channel
    pyre::journal::debug_t channel("reverso.source");

    // sign on
    channel
        << pyre::journal::at(__HERE__)
        << "computing residuals in place"
        << pyre::journal::endl;

    // unpack the number of samples and number of observations
    auto nSamples = predicted->size1;
    auto nObservations = predicted->size2;

    // go through all observations
    for (auto obs=0; obs < nObservations; ++obs) {
        // get the corresponding measurement
        auto actual = gsl_vector_get(_data, obs);
        // go though the samples
        for (auto sample=0; sample < nSamples; ++sample) {
            // get the predicted displacement
            auto pred = gsl_matrix_get(predicted, sample, obs);
            // compute the difference
            auto residual = pred - actual;
            // and store back into the matrix we were handed
            gsl_matrix_set(predicted, sample, obs, residual);
        }
    }

    // all done
    return;
}


// end of file
