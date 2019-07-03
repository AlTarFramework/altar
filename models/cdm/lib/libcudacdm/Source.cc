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
#include <stdexcept>
#include <cuda_runtime.h>
#include <pyre/journal.h>
#include <gsl/gsl_matrix.h>

// my declarations
#include "Source.h"

// make pi
const auto pi = 4*std::atan(1.0);

// meta-methods
// constructor
altar::models::cudacdm::Source::
Source(size_type parameters, size_type samples, size_type observations, double nu):
    _nSamples(samples),
    _nParameters(parameters),
    _nObservations(observations),
    _nu(nu),
    _data(0),
    _locations(0),
    _los(0),
    _oids(0),
    _xIdx(0),
    _yIdx(0),
    _dIdx(0),
    _openingIdx(0),
    _aXIdx(0),
    _aYIdx(0),
    _aZIdx(0),
    _omegaXIdx(0),
    _omegaYIdx(0),
    _omegaZIdx(0),
    _offsetIdx(0),
    _samples(0),
    _predicted(0)
{
    // make a channel
    pyre::journal::debug_t channel("cudacdm.source");

    // compute the amount of memory required to hold the samples
    const size_type sampleFootprint = parameters * samples * sizeof(data_type);
    // allocate device memory for them
    cudaError_t status = cudaMallocManaged(&_samples, sampleFootprint);
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while allocating device memory for the parameter samples: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::bad_alloc();
    }
    // otherwise, tell me
    channel
        << pyre::journal::at(__HERE__)
        << "allocated an arena of " << sampleFootprint << " bytes for the samples"
        << pyre::journal::endl;

    // compute the amount of memory required to hold the predicted displacements
    const size_type displacementsFootprint = samples * observations * sizeof(data_type);
    // allocate device memory for them
    status = cudaMallocManaged(&_predicted, displacementsFootprint);
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while allocating device memory for the predicted displacements: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::bad_alloc();
    }
    // otherwise, tell me
    channel
        << pyre::journal::at(__HERE__)
        << "allocated an arena of " << displacementsFootprint
        << " bytes for the predicted displacements"
        << pyre::journal::endl;

    // compute the amount of memory needed to hold the data
    const size_type dataFootprint = _nObservations * sizeof(data_type);
    // allocate device memory for them
    status = cudaMallocManaged(&_data, dataFootprint);
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while allocating device memory for the observations: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::bad_alloc();
    }
    // otherwise, tell me
    channel
        << pyre::journal::at(__HERE__)
        << "allocated an arena of " << dataFootprint << " bytes for the observations"
        << pyre::journal::endl;

    // we only have (x,y) coordinates for the observation points
    const int locDim = 2;
    // compute the memory footprint of the coordinates of the observation points
    const size_type locationsFootprint = locDim * _nObservations * sizeof(data_type);
    // allocate device memory for them
    status = cudaMallocManaged(&_locations, locationsFootprint);
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while allocating device memory for the location coordinates: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::bad_alloc();
    }
    // otherwise, tell me
    channel
        << pyre::journal::at(__HERE__)
        << "allocated an arena of " << locationsFootprint << " bytes for the observation locations"
        << pyre::journal::endl;

    // we have the 3 components of the unit LOS vectors to the observation point on the ground
    const int losDim = 3;
    // compute the memory footprint of the LOS unit vectors
    const size_type losFootprint = losDim * _nObservations * sizeof(data_type);
    // allocate device memory for them
    status = cudaMallocManaged(&_los, losFootprint);
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while allocating device memory for the location coordinates: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::bad_alloc();
    }
    // otherwise, tell me
    channel
        << pyre::journal::at(__HERE__)
        << "allocated an arena of " << losFootprint << " bytes for the unit LOS vectors"
        << pyre::journal::endl;

    // compute the memory footprint for the dataset membership table
    const size_type oidFootprint = _nObservations * sizeof(size_type);
    // allocate device memory
    status = cudaMallocManaged(&_oids, oidFootprint);
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while allocating device memory for the dataset ids: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::bad_alloc();
    }
    // otherwise, tell me
    channel
        << pyre::journal::at(__HERE__)
        << "allocated an arena of " << oidFootprint << " bytes for the dataset ids"
        << pyre::journal::endl;

}


// destructor
altar::models::cudacdm::Source::
~Source() {
    // make a channel
    pyre::journal::debug_t channel("cudacdm.source");

    // sign on
    channel
        << pyre::journal::at(__HERE__)
        << "deleting source " << this
        << pyre::journal::endl;

    // deallocate device memory
    // if we were handed data
    if (_data) {
        // release it
        cudaFree(_data);
        // tell me
        channel
            << pyre::journal::at(__HERE__)
            << "  released {_data} device memory at" << _data
            << pyre::journal::endl;
    }

    // if we were handed the locations of the observation points
    if (_locations) {
        // release it
        cudaFree(_locations);
        // tell me
        channel
            << pyre::journal::at(__HERE__)
            << "  released {_locations} device memory at" << _locations
            << pyre::journal::endl;
    }

    // if we were handed line of sight vectors
    if (_los) {
        // release it
        cudaFree(_los);
        // tell me
        channel
            << pyre::journal::at(__HERE__)
            << "  released {_los} device memory at" << _los
            << pyre::journal::endl;

    }

    // if we were handed observation data set membership
    if (_oids) {
        // release it
        cudaFree(_oids);
        // tell me
        channel
            << pyre::journal::at(__HERE__)
            << "  released {_oids} device memory at" << _oids
            << pyre::journal::endl;
    }

    // if we were successful in allocating memory for the samples
    if (_samples) {
        // release it
        cudaFree(_samples);
        // tell me
        channel
            << pyre::journal::at(__HERE__)
            << "  released {_samples} device memory at" << _samples
            << pyre::journal::endl;
    }

    // if we were successful in allocating memory for the predicted displacements
    if (_predicted) {
        // release it
        cudaFree(_predicted);
        // tell me
        channel
            << pyre::journal::at(__HERE__)
            << "  released {__predicted} device memory at" << _predicted
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
altar::models::cudacdm::Source::
data(gsl_vector * data) {
    // make a channel
    pyre::journal::debug_t channel("cudacdm.source");

    // compute the memory footprint
    const size_type dataFootprint = _nObservations * sizeof(data_type);
    // move the data from the vector to the device
    cudaError_t status = cudaMemcpy(_data, data->data, dataFootprint, cudaMemcpyHostToDevice);
    // check
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while copying data to the device: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::runtime_error("while copying data to the device");
    }

    // tell me
    channel
        << pyre::journal::at(__HERE__)
        << "attached data from " << _data
        << pyre::journal::endl;

    // all done
    return;
}


void
altar::models::cudacdm::Source::
locations(gsl_matrix * locations) {
    // make a channel
    pyre::journal::debug_t channel("cudacdm.source");

    // we only have the (x,y) coordinates of the observation points on the surface
    const int dim = 2;
    // compute the number of locations
    const size_type nLoc = dim * _nObservations;
    // compute the memory footprint
    const size_type locationsFootprint = nLoc * sizeof(data_type);

    // we want to re-pack the coordinates; allocate a temporary buffer
    data_type * buffer = new data_type[nLoc];
    // go through the three axes
    for (size_type axis=0; axis < dim; ++axis) {
        // and the observations
        for (size_type obs=0; obs < _nObservations; ++obs) {
            // copy the data
            buffer[axis*_nObservations + obs] = gsl_matrix_get(locations, obs, axis);
        }
    }

    // move the data
    cudaError_t status = cudaMemcpy(_locations, buffer, locationsFootprint, cudaMemcpyHostToDevice);
    // clean up
    delete [] buffer;
    // check
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while copying location coordinates to the device: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::runtime_error("while copying location coordinates to the device");
    }

    // tell me
    channel
        << pyre::journal::at(__HERE__)
        << "attached locations from " << _locations
        << pyre::journal::endl;

    // all done
    return;
}


void
altar::models::cudacdm::Source::
los(gsl_matrix * los) {

    // make a channel
    pyre::journal::debug_t channel("cudacdm.source");

    // we have the 3 components of the unit LOS vectors to the observation point on the ground
    const int dim = 3;
    // compute the number of components
    const size_type nLOS = dim * _nObservations;
    // compute the memory footprint
    const size_type losFootprint = nLOS * sizeof(data_type);

    // we want to re-pack the coordinates; allocate a temporary buffer
    data_type * buffer = new data_type[nLOS];
    // go through the three axes
    for (size_type axis=0; axis < dim; ++axis) {
        // and the observations
        for (size_type obs=0; obs < _nObservations; ++obs) {
            // copy the data
            buffer[axis*_nObservations + obs] = gsl_matrix_get(los, obs, axis);
        }
    }

    // move the data
    cudaError_t status = cudaMemcpy(_los, buffer, losFootprint, cudaMemcpyHostToDevice);
    // clean up
    delete [] buffer;
    // check
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while copying LOS components to the device: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::runtime_error("while copying LOS components to the device");
    }

    // tell me
    channel
        << pyre::journal::at(__HERE__)
        << "attached LOS matrix at " << _los
        << pyre::journal::endl;

    // all done
    return;
}


void
altar::models::cudacdm::Source::
oids(const oids_type & oids) {
    // make a channel
    pyre::journal::debug_t channel("cudacdm.source");

    // compute the memory footprint
    const size_type oidFootprint = _nObservations * sizeof(size_type);
    // move the data
    cudaError_t status = cudaMemcpy(_oids, &oids[0], oidFootprint, cudaMemcpyHostToDevice);
    // check
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while copying dataset ids to the device: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::runtime_error("while copying dataset ids to the device");
    }

    // tell me
    channel
        << pyre::journal::at(__HERE__)
        << "attached data set ids to the observations"
        << pyre::journal::endl;

    // all done
    return;
}


void
altar::models::cudacdm::Source::
residuals(gsl_matrix_view * theta, gsl_matrix * residuals) const
{

    // transfer the samples to the device
    _theta(theta);
    // compute the predicted displacements
    _displacements();
    // compute the residuals
    _residuals();
    // harvest the results
    _harvest(residuals);

    // all done
    return;
}


// implementation details
void
altar::models::cudacdm::Source::
_theta(gsl_matrix_view * samples) const
{
    // make a channel
    pyre::journal::debug_t channel("cudacdm.source");

    // compute the total number of values in the sample set
    const size_type nValues = _nSamples * _nParameters;
    // the amount of memory they occupy
    const size_type valueFootprint = nValues * sizeof(data_type);
    // make a buffer to hold them
    data_type * values = new data_type[nValues];
    // go through the samples
    for (size_type sample=0; sample < _nSamples; ++sample) {
        // and all parameters
        for (size_type param=0; param < _nParameters; ++param) {
            // move the values over to the temporary buffer
            values[sample*_nParameters + param] = gsl_matrix_get(&samples->matrix, sample, param);
        }
    }
    // move to the device
    cudaError_t status = cudaMemcpy(_samples, values, valueFootprint, cudaMemcpyHostToDevice);
    // clean up the temporary buffer
    delete [] values;
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while copying samples to the device: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::runtime_error("while copying samples to the device");
    }

    // tell me
    channel
        << pyre::journal::at(__HERE__)
        << "transferred the samples to the device"
        << pyre::journal::endl;

    // all done
    return;
}


void
altar::models::cudacdm::Source::
_harvest(gsl_matrix * residuals) const
{
    // make a channel
    pyre::journal::debug_t channel("cudacdm.source");

    // the number of cells in the results
    const size_type nCells = _nSamples * _nObservations;
    // the amount of memory they occupy
    const size_type dispFootprint = nCells * sizeof(data_type);
    // make some room for the results
    data_type * buffer = new data_type[nCells];
    // harvest the predicted displacements
    cudaError_t status = cudaMemcpy(buffer, _predicted, dispFootprint, cudaMemcpyDeviceToHost);
    // clean up
    delete [] buffer;
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while harvesting residuals from the device: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::runtime_error("while harvesting residuals");
    }
    // go through the observation points
    for (size_type loc=0; loc < _nObservations; ++loc) {
        // and the samples
        for (size_type sample=0; sample < _nSamples; ++sample) {
            // transfer to the matrix
            gsl_matrix_set(residuals, sample, loc, buffer[loc*_nSamples + sample]);
        }
    }

    // all done
    return;
}


// end of file
