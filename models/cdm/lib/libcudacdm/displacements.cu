// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 2013-2019 parasim inc
// all rights reserved
//

// configuration
#include <portinfo>
// math
#include <cmath>
#include <limits>
// cuda
#include <cuda_runtime.h>
#include <math_constants.h>
// external
#include <pyre/journal.h>
#include <gsl/gsl_matrix.h>
// my class declaration
#include "Source.h"

// type aliases
using vec_t = double3;
struct mat_t { double4 rows[3]; };

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
                   std::size_t openingIdx,
                   std::size_t aXIdx,
                   std::size_t aYIdx,
                   std::size_t aZIdx,
                   std::size_t omegaXIdx,
                   std::size_t omegaYIdx,
                   std::size_t omegaZIdx,

                   // the predicted displacements
                   double * predicted
                   );

// helpers
__device__ static
void
RDdispSurf(std::size_t w, std::size_t nSamples, std::size_t nObservations,
           const double * locations, double * los,
           const vec_t & P1, const vec_t & P2, const vec_t & P3, const vec_t & P4,
           double opening, double nu,
           double * results);

__device__ static
vec_t AngSetupFSC(double x, double y,
                  const vec_t & b, const vec_t & PA, const vec_t & PB,
                  double nu);

__device__ static
vec_t AngDisDispSurf(const vec_t & y, double beta, const vec_t & b,
               double nu, double a);
// algebra
__device__ inline static vec_t operator+(const vec_t & v);
__device__ inline static vec_t operator-(const vec_t & v);
__device__ inline static vec_t operator+(const vec_t & v1, const vec_t & v2);
__device__ inline static vec_t operator-(const vec_t & v1, const vec_t & v2);
__device__ inline static vec_t operator*(double a, const vec_t & v);
__device__ inline static vec_t operator*(const vec_t & v, double a);
__device__ inline static vec_t operator/(const vec_t & v, double a);

__device__ inline static mat_t operator*(const mat_t & m1, const mat_t & m2);

__device__ inline static double norm(const vec_t & v);
__device__ inline static double dot(const vec_t & v1, const vec_t & v2);
__device__ inline static vec_t cross(const vec_t & v1, const vec_t & v2);
__device__ inline static mat_t transpose(const mat_t & m);
__device__ inline static vec_t xform(const mat_t & m, const vec_t & v);

// trig
__device__ inline static double sind(double);
__device__ inline static double cosd(double);


// the implementation of the source method
void
altar::models::cudacdm::Source::
_displacements() const
{
    // make a channel
    pyre::journal::debug_t channel("cudacdm.source");

    // show me
    channel
        << pyre::journal::at(__HERE__)
        << "launching the displacements kernel"
        << pyre::journal::endl;

    // if each block has T threads
    const int T = 64;
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
                          _xIdx, _yIdx, _dIdx, _openingIdx,
                          _aXIdx, _aYIdx, _aZIdx,
                          _omegaXIdx, _omegaYIdx, _omegaZIdx,
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
              std::size_t openingIdx,
              std::size_t aXIdx,
              std::size_t aYIdx,
              std::size_t aZIdx,
              std::size_t omegaXIdx,
              std::size_t omegaYIdx,
              std::size_t omegaZIdx,

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

    // constants
    const double eps = 1e-11;
    // get the source location
    auto x = mine[xIdx];
    auto y = mine[yIdx];
    auto depth = mine[dIdx];
    // the opening
    auto opening = mine[openingIdx];
    // the semi axes
    auto aX = mine[aXIdx];
    auto aY = mine[aXIdx+1];
    auto aZ = mine[aXIdx+2];
    // the orientations
    auto omegaX = mine[omegaXIdx];
    auto omegaY = mine[omegaXIdx + 1];
    auto omegaZ = mine[omegaXIdx + 2];

    mat_t Rx = {make_double4(1.,  0.,           0.,           0.),
                make_double4(0.,  cosd(omegaX), sind(omegaX), 0.),
                make_double4(0., -sind(omegaX), cosd(omegaX), 0.)};

    mat_t Ry = {make_double4(cosd(omegaY), 0., -sind(omegaY), 0.),
                make_double4(0.,           1.,  0.,           0.),
                make_double4(sind(omegaY), 0.,  cosd(omegaY), 0.)};

    mat_t Rz = {make_double4( cosd(omegaZ), sind(omegaZ), 0., 0.),
                make_double4(-sind(omegaZ), cosd(omegaZ), 0., 0.),
                make_double4( 0.,           0.,           1., 0.)};

    // the rotation matrix
    mat_t R = Rz * (Ry * Rx);
    // extract its three columns
    vec_t R_0 = { R.rows[0].x, R.rows[1].x, R.rows[2].x };
    vec_t R_1 = { R.rows[0].y, R.rows[1].y, R.rows[2].y };
    vec_t R_2 = { R.rows[0].z, R.rows[1].z, R.rows[2].z };

    // the centroid
    vec_t P0 = { x, y, -depth };

    vec_t P1 = P0 + (aY*R_1 + aZ*R_2)/2;
    vec_t P2 = P1 - aY*R_1;
    vec_t P3 = P2 - aZ*R_2;
    vec_t P4 = P1 - aZ*R_2;

    vec_t Q1 = P0 + (aZ*R_2 - aX*R_0)/2;
    vec_t Q2 = Q1 + aX*R_0;
    vec_t Q3 = Q2 - aZ*R_2;
    vec_t Q4 = Q1 - aZ*R_2;

    vec_t R1 = P0 + (aX*R_0 + aY*R_1)/2;
    vec_t R2 = R1 - aX*R_0;
    vec_t R3 = R2 - aY*R_1;
    vec_t R4 = R1 - aY*R_1;

    // zero out my slice of the results
    for (auto loc=0; loc<nObservations; ++loc) {
        predicted[loc*nSamples + w] = 0;
    }

    // dispatch the various cases
    if (std::abs(aX) < eps && std::abs(aY) > eps && std::abs(aZ) > eps) {
        RDdispSurf(w, nSamples, nObservations, locations, los,
                   P1, P2, P3, P4, opening, nu, predicted);
    } else if (std::abs(aX) > eps && std::abs(aY) < eps && std::abs(aZ) > eps) {
        RDdispSurf(w, nSamples, nObservations, locations, los,
                   Q1, Q2, Q3, Q4, opening, nu, predicted);
    } else if (std::abs(aX) > eps && std::abs(aY) > eps && std::abs(aZ) < eps) {
        RDdispSurf(w, nSamples, nObservations, locations, los,
                   R1, R2, R3, R4, opening, nu, predicted);
    } else {
    }

    // all done
    return;
}

// helpers
__device__ static
void
RDdispSurf(std::size_t w, std::size_t nSamples, std::size_t nObservations,
           const double * locations, double * los,
           const vec_t & P1, const vec_t & P2, const vec_t & P3, const vec_t & P4,
           double opening, double nu,
           double * results) {
    // opening
    auto V = cross(P2-P1, P4-P1);
    auto b = opening * V/norm(V);

    for (auto loc=0; loc<nObservations; ++loc) {
        // unpack the observation point coordinates
        auto x = locations[loc];
        auto y = locations[nObservations + loc];
        // compute
        auto u1 = AngSetupFSC(x,y, b, P1,P2, nu);
        auto u2 = AngSetupFSC(x,y, b, P2,P3, nu);
        auto u3 = AngSetupFSC(x,y, b, P3,P4, nu);
        auto u4 = AngSetupFSC(x,y, b, P4,P1, nu);

        // assemble
        auto u = u1 + u2 + u3 + u4;
        // compute the unit LOS vector
        vec_t n = { los[loc], los[nObservations + loc], los[2*nObservations + loc] };
        // project the displacement to the LOS
        auto uLOS = dot(u, n);
        // save by accumulating my contribution to the slot
        // N.B.: note the "+=": the general case call this function three times
        results[loc*nSamples + w] += uLOS;
    }

    // all done
    return;
};

__device__ static
vec_t AngSetupFSC(double x, double y,
                  const vec_t & b, const vec_t & PA, const vec_t & PB,
                  double nu) {
    const double pi = CUDART_PI;
    vec_t SideVec = PB - PA;
    vec_t eZ = {0, 0, 1};
    auto beta = std::acos(dot(SideVec, eZ) / norm(SideVec));

    if (std::abs(beta) < 1e-12 || std::abs(pi - beta) < 1e-12) {
        return { 0,0,0 };
    }

    vec_t ey1 = { SideVec.x, SideVec.y, 0 };
    ey1 = ey1 / norm(ey1);
    vec_t ey3 = -eZ;
    vec_t ey2 = cross(ey3, ey1);

    mat_t A = { ey1.x, ey1.y, ey1.z,
                ey2.x, ey2.y, ey2.z,
                ey3.x, ey3.y, ey3.z};

    vec_t adcsA = xform(A, {x-PA.x, y-PA.y, -PA.z});
    vec_t adcsAB = xform(A, SideVec);
    vec_t adcsB = adcsA - adcsAB;

    // transform the slip vector
    vec_t bADCS = xform(A, b);

    vec_t vA, vB;
    // distinguish the two configurations
    if (beta*adcsA.x > 0) {
        // configuration I
        vA = AngDisDispSurf(adcsA, -pi+beta, b, nu, -PA.z);
        vB = AngDisDispSurf(adcsB, -pi+beta, b, nu, -PB.z);
    } else {
        // configuration II
        vA = AngDisDispSurf(adcsA, beta, b, nu, -PB.z);
        vB = AngDisDispSurf(adcsB, beta, b, nu, -PB.z);
    }

    vec_t v = xform(transpose(A), vB - vA);

    return v;
}

__device__ static
vec_t AngDisDispSurf(const vec_t & y, double beta, const vec_t & b,
                     double nu, double a)
{
    // constants
    const double pi = CUDART_PI;
    // unpack
    auto b1 = b.x;
    auto b2 = b.y;
    auto b3 = b.z;
    auto y1 = y.x;
    auto y2 = y.y;
    // common factors
    auto sinB = std::sin(beta);
    auto cosB = std::cos(beta);
    auto cotB = 1 / std::tan(beta);
    auto z1 = y1*cosB + a*sinB;
    auto z3 = y1*sinB - a*cosB;
    auto r2 = y1*y1 + y2*y2 + a*a;
    auto r = std::sqrt(r2);

    // the Burgers function
    auto Fi = 2*std::atan2(y2, (r+a)/std::tan(beta/2) - y1);

    auto v1b1 = b1/2/pi*((1-(1-2*nu)*cotB*cotB)*Fi +
                         y2/(r+a)*((1-2*nu)*(cotB+y1/2/(r+a))-y1/r) -
                         y2*(r*sinB-y1)*cosB/r/(r-z3));

    auto v2b1 = b1/2/pi*((1-2*nu)*((.5+cotB*cotB)*std::log(r+a)-cotB/sinB*std::log(r-z3)) -
                         1./(r+a)*((1-2*nu)*(y1*cotB-a/2-y2*y2/2/(r+a))+y2*y2/r) +
                         y2*y2*cosB/r/(r-z3));

    auto v3b1 = b1/2/pi*((1-2*nu)*Fi*cotB+y2/(r+a)*(2*nu+a/r) - y2*cosB/(r-z3)*(cosB+a/r));

    auto v1b2 = b2/2/pi*(-(1-2*nu)*((.5-cotB*cotB)*std::log(r+a) + cotB*cotB*cosB*std::log(r-z3) ) -
                         1/(r+a)*((1-2*nu)*(y1*cotB+.5*a+y1*y1/2/(r+a)) - y1*y1/r) +
                         z1*(r*sinB-y1)/r/(r-z3));

    auto v2b2 = b2/2/pi*((1+(1-2*nu)*cotB*cotB)*Fi -
                         y2/(r+a)*((1-2*nu)*(cotB+y1/2/(r+a))-y1/r) -
                         y2*z1/r/(r-z3));

    auto v3b2 = b2/2/pi*(-(1-2*nu)*cotB*(std::log(r+a)-cosB*std::log(r-z3)) -
                         y1/(r+a)*(2*nu+a/r) + z1/(r-z3)*(cosB+a/r));

    auto v1b3 = b3/2/pi*(y2*(r*sinB-y1)*sinB/r/(r-z3));
    auto v2b3 = b3/2/pi*(-y2*y2*sinB/r/(r-z3));
    auto v3b3 = b3/2/pi*(Fi + y2*(r*cosB+a)*sinB/r/(r-z3));

    auto v1 = v1b1 + v1b2 + v1b3;
    auto v2 = v2b1 + v2b2 + v2b3;
    auto v3 = v3b1 + v3b2 + v3b3;

    return {v1, v2, v3};
}



// algebra
__device__ inline static
vec_t operator+(const vec_t & v) {
    return v;
}

__device__ inline static
vec_t operator-(const vec_t & v) {
    return -1.0 *v;
};

__device__ inline static
vec_t operator+(const vec_t & v1, const vec_t & v2) {
    return { v1.x + v2.x, v1.y + v2.y, v1.z + v2.z };
};

__device__ inline static
vec_t operator-(const vec_t & v1, const vec_t & v2) {
    return { v1.x - v2.x, v1.y - v2.y, v1.z - v2.z };
};

__device__ inline static
vec_t operator*(double a, const vec_t & v) {
    return { a*v.x, a*v.y, a*v.z };
};

__device__ inline static
vec_t operator*(const vec_t & v, double a) {
    return { a*v.x, a*v.y, a*v.z };
}

__device__ inline static
vec_t operator/(const vec_t & v, double a) {
    return { v.x/a, v.y/a, v.z/a };
};

__device__ inline static
mat_t operator*(const mat_t & m1, const mat_t & m2) {
    mat_t m;

    m.rows[0] = make_double4(
                             // m[0,0]
                             m1.rows[0].x*m2.rows[0].x +
                             m1.rows[0].y*m2.rows[1].x +
                             m1.rows[0].z*m2.rows[2].x,
                             // m[0,1]
                             m1.rows[0].x*m2.rows[0].y +
                             m1.rows[0].y*m2.rows[1].y +
                             m1.rows[0].z*m2.rows[2].y,
                             // m[0,2]
                             m1.rows[0].x*m2.rows[0].z +
                             m1.rows[0].y*m2.rows[1].z +
                             m1.rows[0].z*m2.rows[2].z,
                             // filler
                             0);

    m.rows[1] = make_double4(
                             // m[1,0]
                             m1.rows[1].x*m2.rows[0].x +
                             m1.rows[1].y*m2.rows[1].x +
                             m1.rows[1].z*m2.rows[2].x,
                             // m[1,1]
                             m1.rows[1].x*m2.rows[0].y +
                             m1.rows[1].y*m2.rows[1].y +
                             m1.rows[1].z*m2.rows[2].y,
                             // m[1,2]
                             m1.rows[1].x*m2.rows[0].z +
                             m1.rows[1].y*m2.rows[1].z +
                             m1.rows[1].z*m2.rows[2].z,
                             // filler
                             0);

    m.rows[2] = make_double4(
                             // m[2,0]
                             m1.rows[2].x*m2.rows[0].x +
                             m1.rows[2].y*m2.rows[1].x +
                             m1.rows[2].z*m2.rows[2].x,
                             // m[2,1]
                             m1.rows[2].x*m2.rows[0].y +
                             m1.rows[2].y*m2.rows[1].y +
                             m1.rows[2].z*m2.rows[2].y,
                             // m[2,2]
                             m1.rows[2].x*m2.rows[0].z +
                             m1.rows[2].y*m2.rows[1].z +
                             m1.rows[2].z*m2.rows[2].z,
                             // filler
                             0);

    return m;
}

__device__ static inline
double norm(const vec_t & v) {
    return std::sqrt(v.x*v.x + v.y*v.y + v.z*v.z);
}

__device__ static inline
double dot(const vec_t & v1, const vec_t & v2) {
    return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z;
}

__device__ static inline
vec_t cross(const vec_t & v1, const vec_t & v2) {
    return { v1.y*v2.z - v1.z*v2.y, v1.z*v2.x - v1.x*v2.z, v1.x*v2.y - v1.y*v2.x };
}

__device__ static inline
mat_t transpose(const mat_t & m) {
    return {make_double4(m.rows[0].x, m.rows[1].x, m.rows[2].x, 0.),
            make_double4(m.rows[0].y, m.rows[1].y, m.rows[2].y, 0.),
            make_double4(m.rows[0].z, m.rows[1].z, m.rows[2].z, 0.)};
}

__device__ static inline
vec_t xform(const mat_t & m, const vec_t & v) {
    return {m.rows[0].x*v.x + m.rows[0].y*v.y + m.rows[0].z*v.z,
            m.rows[1].x*v.x + m.rows[1].y*v.y + m.rows[1].z*v.z,
            m.rows[2].x*v.x + m.rows[2].y*v.y + m.rows[2].z*v.z};
}

__device__ static inline
double sind(double omega) {
    return std::sin(omega * 180/CUDART_PI);
}

__device__ static inline
double cosd(double omega) {
    return std::cos(omega * 180/CUDART_PI);
}

// end of file
