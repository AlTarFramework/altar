// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 2013-2018 parasim inc
// all rights reserved
//

// configuration
#include <portinfo>
// external
#include <cmath>
#include <pyre/journal.h>
#include <gsl/gsl_matrix.h>

// my declarations
#include "Source.h"

// make pi
const auto pi = 4*std::atan(1.0);

// meta-methods
// destructor
altar::models::cdm::Source::
~Source() {
    // make a channel
    pyre::journal::debug_t channel("cdm.source");

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
altar::models::cdm::Source::
displacements(gsl_matrix_view * samples, gsl_matrix * predicted) const {
    // pull the number of samples and parameters from the shape of the {sample} matrix
    auto nSamples = samples->matrix.size1;
    auto nParameters = samples->matrix.size2;

    // go through all the samples
    for (auto sample=0; sample<nSamples; ++sample) {
        // unpack the parameters
        auto xSrc = gsl_matrix_get(&samples->matrix, sample, _xIdx);
        auto ySrc = gsl_matrix_get(&samples->matrix, sample, _yIdx);
        auto dSrc = gsl_matrix_get(&samples->matrix, sample, _dIdx);
        auto openingSrc = std::pow(10, gsl_matrix_get(&samples->matrix, sample, _openingIdx));

    }

    // all done
    return;
}


void
altar::models::cdm::Source::
residuals(gsl_matrix * predicted) const {
    // make a channel
    pyre::journal::debug_t channel("cdm.source");

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
