// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 2013-2020 parasim inc
// all rights reserved
//

// configuration
#include <portinfo>
// cuda
#include <cuda_runtime.h>
// external
#include <pyre/journal.h>
#include <gsl/gsl_matrix.h>
// my class declaration
#include "Source.h"


// the displacement kernel
__global__ static
void residuals(
               // the sizes of things
               std::size_t nParameters,
               std::size_t nSamples,
               std::size_t nObservations,

               // the current sample set
               double * theta,
               // the observed displacements
               double * data,
               // the dataset id map
               std::size_t * oids,

               // the shift parameter index within a sample
               std::size_t offsetIdx,

               // the predicted displacements
               double * predicted
               );

// the implementation of the source method
void
altar::models::cudacdm::Source::
_residuals() const
{
    // make a channel
    pyre::journal::debug_t channel("cudacdm.source");

    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "launching the residuals kernel"
        << pyre::journal::endl;

    // if each block has T threads
    const int T = 128;
    // then we need B blocks to process all the chains
    const int B = _nSamples/T + (_nSamples % T ? 1 : 0);

    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "residuals: launching " << B << " blocks of " << T << " threads each"
        << pyre::journal::endl;

    // compute the displacements
    ::residuals<<<B, T>>>(
                          _nParameters, _nSamples, _nObservations,
                          _samples, _data, _oids,
                          _offsetIdx,
                          _predicted
                          );

    // wait for the device to finish
    cudaError_t status = cudaDeviceSynchronize();
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudacdm.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while computing the residuals: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::runtime_error("error while computing residuals");
    }

    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "residuals kernel done"
        << pyre::journal::endl;

    // all done
    return;
}


// the kernel
__global__ static
void
residuals(
              // the sizes of things
              std::size_t nParameters,
              std::size_t nSamples,
              std::size_t nObservations,

              // the current sample set
              double * theta,
              // the observed displacements
              double * data,
              // the dataset id map
              std::size_t * oids,

              // the shift parameter index within a sample
              std::size_t offsetIdx,

              // the predicted displacements
              double * predicted
              )
{
    // build the workload descriptors
    // global
    // std::size_t B = gridDim.x; // number of blocks
    std::size_t T = blockDim.x;   // number of threads per block
    // std::size_t W = B*T;       // total number of workers
    // local
    std::size_t b = blockIdx.x;   // my block id
    std::size_t t = threadIdx.x;  // my thread id within my block
    std::size_t w = b*T + t;      // my worker id

    // if we have processed all the samples
    if (w >= nSamples) {
        // there is nothing for me to do
        return;
    }

    // compute the beginning of my sample
    auto * mine = theta + w*nParameters;

    // go through the observation points
    for (std::size_t loc=0; loc < nObservations; ++loc) {
        // get the observation
        auto observed = data[loc];
        // lookup  the overall shift that corresponds to this observation
        auto shift = mine[offsetIdx + oids[loc]];
        // adjust the value
        predicted[loc*nSamples + w] -= observed + shift;
    }

    // all done
    return;
}


// end of file
