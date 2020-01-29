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
void displacements(
                   // the sizes of things
                   std::size_t nParameters,
                   std::size_t nSamples,
                   std::size_t nObservations,

                   // the elastic constant of the medium
                   double nu,

                   // the current sample set
                   double * theta,
                   // the coordinates of the observation points
                   double * locations,
                   // and the components of the corresponding LOS unit vectors
                   double * los,

                   // the parameter layout within a sample
                   std::size_t xIdx,
                   std::size_t yIdx,
                   std::size_t dIdx,
                   std::size_t sIdx,

                   // the predicted displacements
                   double * predicted
                   );

// the implementation of the source method
void
altar::models::cudamogi::Source::
_displacements() const
{
    // make a channel
    pyre::journal::debug_t channel("cudamogi.source");

    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "launching the displacements kernel"
        << pyre::journal::endl;

    // if each block has T threads
    const int T = 128;
    // then we need B blocks to process all the chains
    const int B = _nSamples/T + (_nSamples % T ? 1 : 0);

    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "displacements: launching " << B << " blocks of " << T << " threads each"
        << pyre::journal::endl;

    // compute the displacements
    ::displacements<<<B, T>>>(
                          _nParameters, _nSamples, _nObservations,
                          _nu,
                          _samples, _locations, _los,
                          _xIdx, _yIdx, _dIdx, _sIdx,
                          _predicted
                          );

    // wait for the device to finish
    cudaError_t status = cudaDeviceSynchronize();
    // if something went wrong
    if (status != cudaSuccess) {
        // make a channel
        pyre::journal::error_t error("cudamogi.source");
        // complain
        error
            << pyre::journal::at(__HERE__)
            << "while computing the displacements: "
            << cudaGetErrorName(status) << " (" << status << ")"
            << pyre::journal::endl;
        // and bail
        throw std::runtime_error("error while computing displacements");
    }

    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "displacements kernel done"
        << pyre::journal::endl;

    // all done
    return;
}


// the kernel
__global__ static
void
displacements(
              // the sizes of things
              std::size_t nParameters,
              std::size_t nSamples,
              std::size_t nObservations,

              // the elastic constant of the medium
              double nu,

              // the current sample set
              double * theta,
              // the coordinates of the observation points
              double * locations,
              // and the components of the corresponding LOS unit vectors
              double * los,

              // the parameter layout within a sample
              std::size_t xIdx,
              std::size_t yIdx,
              std::size_t dIdx,
              std::size_t sIdx,

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

    // i need this
    const auto pi = 4*std::atan(1.0);
    // compute the beginning of my sample
    auto * mine = theta + w*nParameters;

    // get the source location
    auto xSrc = mine[xIdx];
    auto ySrc = mine[yIdx];
    auto dSrc = mine[dIdx];
    // the source strength
    auto sSrc = std::pow(10, mine[sIdx]);

    // go through each observation location
    for (std::size_t loc=0; loc<nObservations; ++loc) {
        // unpack the location of the observation point
        auto xObs = locations[loc];
        auto yObs = locations[nObservations+loc];

        // compute the displacement from the source to the observation point
        auto x = xSrc - xObs;
        auto y = ySrc - yObs;
        auto d = dSrc;

        // compute the distance
        auto R  = std::sqrt(x*x + y*y +d*d);
        // compute the elastic response
        auto C = (nu - 1) * sSrc / pi;
        // form the scaling term
        auto CR3 = C / (R*R*R);

        // compute the components of the unit LOS vector
        auto nx = los[loc];
        auto ny = los[nObservations + loc];
        auto nz = los[2*nObservations + loc];

        // project the displacement to the LOS
        auto u = (x*nx + y*ny - d*nz) * CR3;
        // save
        predicted[loc*nSamples + w] = u;
    }

    // all done
    return;
}


// end of file
