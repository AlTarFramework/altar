// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 2013-2019 parasim inc
// all rights reserved
//

// externals
#include <cmath>
#include <limits>
#include <array>
#include <stdexcept>
#include <gsl/gsl_matrix.h>
// declarations
#include "cdm.h"

namespace altar {
    namespace models {
        namespace cdm {

            // type definitions
            using vec_t = std::array<double, 3>;
            using mat_t = std::array<double, 9>;
            // constants
            // pi
            const auto pi = 4*std::atan(1.0);
            // machine epsilon
            const auto eps = std::numeric_limits<double>::epsilon();

            // local helpers
            static void
            RDdispSurf(int sample,
                       const gsl_matrix * locations, const gsl_matrix * los,
                       const vec_t & P1, const vec_t & P2, const vec_t & P3, const vec_t & P4,
                       double opening, double nu,
                       gsl_matrix * results);

            static vec_t
            AngSetupFSC(double x, double y,
                        const vec_t & b, const vec_t & PA, const vec_t & PB,
                        double nu);

            static vec_t
            AngDisDispSurf(const vec_t & y, double beta, const vec_t & b,
                           double nu, double a);

            // algebra
            inline static vec_t operator+(const vec_t &);
            inline static vec_t operator-(const vec_t &);

            inline static vec_t operator+(const vec_t &, const vec_t &);
            inline static vec_t operator-(const vec_t &, const vec_t &);

            inline static vec_t operator*(double, const vec_t &);
            inline static vec_t operator*(const vec_t &, double);
            inline static vec_t operator/(const vec_t &, double);

            inline static mat_t operator*(const mat_t &, const mat_t &);

            inline static double norm(const vec_t &);
            inline static double dot(const vec_t &, const vec_t &);
            inline static vec_t cross(const vec_t &, const vec_t &);

            inline static mat_t transpose(const mat_t & m);

            inline static vec_t xform(const mat_t & m, const vec_t & v);

            // trig
            inline double sin(double);
            inline double cos(double);
        }
    }
}

// the displacement calculator
// definitions
void
altar::models::cdm::
cdm(int sample,
    const gsl_matrix * locations, const gsl_matrix * los,
    double x, double y, double depth,
    double aX, double aY, double aZ,
    double omegaX, double omegaY, double omegaZ,
    double opening,
    double nu,
    gsl_matrix * predicted)
{
    // convert semi-axes to axes
    aX *= 2;
    aY *= 2;
    aZ *= 2;

    // short circuit the trivial case
    if (std::abs(aX) < eps && std::abs(aY) < eps && std::abs(aZ) < eps) {
        // no displacements
        gsl_matrix_set_zero(predicted);
        // all done
        return;
    }

    // the axis specific coordinate matrices
    mat_t Rx = {1.,  0.,          0.,
                0.,  cos(omegaX), sin(omegaX),
                0., -sin(omegaX), cos(omegaX) };

    mat_t Ry = {cos(omegaY), 0., -sin(omegaY),
                0.,          1.,  0.,
                sin(omegaY), 0.,  cos(omegaY) };

    mat_t Rz = { cos(omegaZ), sin(omegaZ), 0.,
                -sin(omegaZ), cos(omegaZ), 0.,
                 0.,         0.,           1.};

    // the coordinate rotation matrix
    mat_t R  = Rz * (Ry * Rx);
    // extract its three columns
    vec_t R_0 = { R[0],   R[3],   R[6] };
    vec_t R_1 = { R[0+1], R[3+1], R[6+1] };
    vec_t R_2 = { R[0+2], R[3+2], R[6+2] };

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

    // check that all z components are negative
    if (P1[2] > 0 || P2[2] > 0 || P3[2] > 0 || P4[2] > 0 ||
        Q1[2] > 0 || Q2[2] > 0 || Q3[2] > 0 || Q4[2] > 0 ||
        R1[2] > 0 || R2[2] > 0 || R3[2] > 0 || R4[2] > 0) {
        // complain...
        throw std::domain_error("the CDM must be below the surface");
    }

    // dispatch the various cases
    if (std::abs(aX) < eps && std::abs(aY) > eps && std::abs(aZ) > eps) {
        RDdispSurf(sample, locations, los, P1, P2, P3, P4, opening, nu, predicted);
    } else if (std::abs(aX) > eps && std::abs(aY) < eps && std::abs(aZ) > eps) {
        RDdispSurf(sample, locations, los, Q1, Q2, Q3, Q4, opening, nu, predicted);
    } else if (std::abs(aX) > eps && std::abs(aY) > eps && std::abs(aZ) < eps) {
        RDdispSurf(sample, locations, los, R1, R2, R3, R4, opening, nu, predicted);
    } else {
        RDdispSurf(sample, locations, los, P1, P2, P3, P4, opening, nu, predicted);
        RDdispSurf(sample, locations, los, Q1, Q2, Q3, Q4, opening, nu, predicted);
        RDdispSurf(sample, locations, los, R1, R2, R3, R4, opening, nu, predicted);
    }

    // all done
    return;
}

// implementations
static void
altar::models::cdm::
RDdispSurf(int sample,
           const gsl_matrix * locations, const gsl_matrix * los,
           const vec_t & P1, const vec_t & P2, const vec_t & P3, const vec_t & P4,
           double opening, double nu,
           gsl_matrix * results) {
    // cross
    auto V = cross(P2-P1, P4-P1);
    auto b = opening * V/norm(V);

    // go through each location
    for (auto loc=0; loc<locations->size1; ++loc) {
        // unpack the observation point coordinates
        auto x = gsl_matrix_get(locations, loc, 0);
        auto y = gsl_matrix_get(locations, loc, 1);
        // compute
        auto u1 = AngSetupFSC(x,y, b, P1, P2, nu);
        auto u2 = AngSetupFSC(x,y, b, P2, P3, nu);
        auto u3 = AngSetupFSC(x,y, b, P3, P4, nu);
        auto u4 = AngSetupFSC(x,y, b, P4, P1, nu);

        // assemble
        auto u = u1 + u2 + u3 + u4;
        // compute the unit LOS vector
        vec_t n = { gsl_matrix_get(los, loc, 0),
                    gsl_matrix_get(los, loc, 1),
                    gsl_matrix_get(los, loc, 2) };

        // project the displacement to the LOS
        auto uLOS = dot(u, n);
        // save by accumulating my contribution to the slot
        // N.B.: note the "+=": the general case call this function three times
        // get the current value
        auto current = gsl_matrix_get(results, sample, loc);
        // update
        current += uLOS;
        // save
        gsl_matrix_set(results, sample, loc, current);
    }

    // all done
    return;
};

static
altar::models::cdm::vec_t
altar::models::cdm::
AngSetupFSC(double x, double y,
            const vec_t & b, const vec_t & PA, const vec_t & PB,
            double nu) {
    vec_t SideVec = PB - PA;
    vec_t eZ = {0, 0, 1};
    auto beta = std::acos(dot(SideVec, eZ) / norm(SideVec));

    if (std::abs(beta) < eps || std::abs(pi - beta) < eps) {
        return { 0,0,0 };
    }

    vec_t ey1 = { SideVec[0], SideVec[1], 0 };
    ey1 = ey1 / norm(ey1);
    vec_t ey3 = -eZ;
    vec_t ey2 = cross(ey3, ey1);

    mat_t A = { ey1[0], ey1[1], ey1[2],
                ey2[0], ey2[1], ey2[2],
                ey3[0], ey3[1], ey3[2]};

    vec_t adcsA = xform(A, {x-PA[0], y-PA[1], -PA[2]});
    vec_t adcsAB = xform(A, SideVec);
    vec_t adcsB = adcsA - adcsAB;

    // transform the slip vector
    vec_t bADCS = xform(A, b);

    vec_t vA, vB;
    // distinguish the two configurations
    if (beta*adcsA[0] > 0) {
        // configuration I
        vA = AngDisDispSurf(adcsA, -pi+beta, b, nu, -PA[2]);
        vB = AngDisDispSurf(adcsB, -pi+beta, b, nu, -PB[2]);
    } else {
        // configuration II
        vA = AngDisDispSurf(adcsA, beta, b, nu, -PB[2]);
        vB = AngDisDispSurf(adcsB, beta, b, nu, -PB[2]);
    }

    vec_t v = xform(transpose(A), vB - vA);

    return v;
}

static
altar::models::cdm::vec_t
altar::models::cdm::
AngDisDispSurf(const vec_t & y, double beta, const vec_t & b,
               double nu, double a)
{
    // unpack
    auto b1 = b[0];
    auto b2 = b[1];
    auto b3 = b[2];
    auto y1 = y[0];
    auto y2 = y[1];
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
inline static
altar::models::cdm::vec_t
altar::models::cdm::
operator+(const vec_t & v) {
    return v;
}

inline static
altar::models::cdm::vec_t
altar::models::cdm::
operator-(const vec_t & v) {
    return -1.0*v;
}

inline static
altar::models::cdm::vec_t
altar::models::cdm::
operator+(const vec_t & v1, const vec_t & v2) {
    return {v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]};
}

inline static
altar::models::cdm::vec_t
altar::models::cdm::
operator-(const vec_t & v1, const vec_t & v2) {
    return {v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]};
}

inline static
altar::models::cdm::vec_t
altar::models::cdm::
operator*(double a, const vec_t & v) {
    return {a*v[0], a*v[1], a*v[2]};
}

inline static
altar::models::cdm::vec_t
altar::models::cdm::
operator*(const vec_t & v, double a) {
    return {v[0]*a, v[1]*a, v[2]*a};
}

inline static
altar::models::cdm::vec_t
altar::models::cdm::
operator/(const vec_t & v, double a) {
    return {v[0]/a, v[1]/a, v[2]/a};
}

inline static
altar::models::cdm::mat_t
altar::models::cdm::
operator*(const mat_t & m1, const mat_t & m2) {
    return { m1[0]*m2[0] + m1[1]*m2[3] + m1[2]*m2[6],
             m1[0]*m2[1] + m1[1]*m2[4] + m1[2]*m2[7],
             m1[0]*m2[2] + m1[1]*m2[5] + m1[2]*m2[8],

             m1[3]*m2[0] + m1[4]*m2[3] + m1[5]*m2[6],
             m1[3]*m2[1] + m1[4]*m2[4] + m1[5]*m2[7],
             m1[3]*m2[2] + m1[4]*m2[5] + m1[5]*m2[8],

             m1[6]*m2[0] + m1[7]*m2[3] + m1[8]*m2[6],
             m1[6]*m2[1] + m1[7]*m2[4] + m1[8]*m2[7],
             m1[6]*m2[2] + m1[7]*m2[5] + m1[8]*m2[8] };
};

inline static
double
altar::models::cdm::
norm(const vec_t & v) {
    return std::sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]);
}

inline static
double
altar::models::cdm::
dot(const vec_t & v1, const vec_t & v2) {
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2];
}

inline static
altar::models::cdm::vec_t
altar::models::cdm::
cross(const vec_t & v1, const vec_t & v2) {
    return { v1[1]*v2[2] - v1[2]*v2[1], v1[2]*v2[0] - v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0] };
}

inline static
altar::models::cdm::mat_t
altar::models::cdm::
transpose(const mat_t & m) {
    return {m[0], m[3], m[6],
            m[1], m[4], m[7],
            m[2], m[5], m[8]};
};

inline static
altar::models::cdm::vec_t
altar::models::cdm::
xform(const mat_t & m, const vec_t & v) {
    return {m[0]*v[0] + m[1]*v[1] + m[2]*v[2],
            m[3]*v[0] + m[4]*v[1] + m[5]*v[2],
            m[6]*v[0] + m[7]*v[1] + m[8]*v[2]};
};

// trig
inline
double
altar::models::cdm::
sin(double omega) {
    return std::sin(omega * pi/180);
};

inline
double
altar::models::cdm::
cos(double omega) {
    return std::cos(omega * pi/180);
};

// end-of-file
