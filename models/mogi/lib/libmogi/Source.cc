// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 2013-2019 parasim inc
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
altar::models::mogi::Source::
~Source() {
    // make a channel
    pyre::journal::debug_t channel("mogi.source");

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
altar::models::mogi::Source::
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
        auto sSrc = std::pow(10, gsl_matrix_get(&samples->matrix, sample, _sIdx));

        // go through the locations
        for (auto loc=0; loc<_locations->size1; ++loc) {
            // unpack the location of the observation point
            auto xObs = gsl_matrix_get(_locations, loc, 0);
            auto yObs = gsl_matrix_get(_locations, loc, 1);

            // compute the displacement from the source to the observation point
            auto x = xSrc - xObs;
            auto y = ySrc - yObs;
            auto d = dSrc;
            // turn it into a distance
            auto R = std::sqrt(x*x + y*y + d*d);

            // compute the elastic response
            auto C = (_nu - 1) * sSrc / pi;

            // put it together
            auto CR3 = C / (R*R*R);

            // compute the components of the unit LOS vector
            auto nx = gsl_matrix_get(_los, loc, 0);
            auto ny = gsl_matrix_get(_los, loc, 1);
            auto nz = gsl_matrix_get(_los, loc, 2);

            // compute the expected displacement
            auto u = (x*nx + y*ny - d*nz) * CR3;
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
altar::models::mogi::Source::
residuals(gsl_matrix * predicted) const {
    // make a channel
    pyre::journal::debug_t channel("mogi.source");

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
