// -*- C++ -*-
//
// eric m. gurrola <eric.m.gurrola@jpl.nasa.gov>
// (c) 2019 jet propulsion lab, california institute of technology
// all rights reserved
//

// externals
#include <cmath>
#include <limits>
#include <array>
#include <stdexcept>
#include <gsl/gsl_matrix.h>
// declarations
#include "reverso.h"

namespace altar {
    namespace models {
        namespace reverso {

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
            reverso(int sample,
                       const gsl_matrix * locations, const gsl_matrix * los,
                       double dPs0, double dPd0,
                       double x0, double y0, double t0,
                       double as, double ac, double ad,
                       double hs, double hd, double qin,
                       double g, double Gsm, double nu, double mu, double drho,
                       gsl_matrix * results);

            static vec_t
            Urmat(double x, double y, double t,
                        const vec_t & b, const vec_t & PA, const vec_t & PB,
                        double nu);

        }
    }
}

// the displacement calculator
// definitions
void
altar::models::reverso::
reverso(int sample,
    const gsl_matrix * locations, const gsl_matrix * los,
    double dPs0, double dPd0,
    double x0, double y0, double t0,
    double as, double ac, double ad,
    double hs, double hd, double qin,
    double g, double Gsm, double nu, double mu, double drho,
    gsl_matrix * predicted)
{
    // Initial conditions: shallow and deep reservoirs overpressure in Pa at t=0
    dPs[0] = dPs0;
    dPd[0] = dPd0;

    // short circuit the trivial case
    if (as < eps || ac < eps || ad < eps ||
        hs < eps || hd < eps || qin < eps) {
        // at least one of the reservoirs or connecting tube or their depths or the
        // input magma flux is too small or negative
        gsl_matrix_set_zero(predicted);
        // all done
        return;
    }


    // all done
    return;
}


// algebra
inline static
altar::models::reverso::vec_t
altar::models::reverso::
operator+(const vec_t & v) {
    return v;
}

inline static
altar::models::reverso::vec_t
altar::models::reverso::
operator-(const vec_t & v) {
    return -1.0*v;
}

inline static
altar::models::reverso::vec_t
altar::models::reverso::
operator+(const vec_t & v1, const vec_t & v2) {
    return {v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]};
}

inline static
altar::models::reverso::vec_t
altar::models::reverso::
operator-(const vec_t & v1, const vec_t & v2) {
    return {v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]};
}

inline static
altar::models::reverso::vec_t
altar::models::reverso::
operator*(double a, const vec_t & v) {
    return {a*v[0], a*v[1], a*v[2]};
}

inline static
altar::models::reverso::vec_t
altar::models::reverso::
operator*(const vec_t & v, double a) {
    return {v[0]*a, v[1]*a, v[2]*a};
}

inline static
altar::models::reverso::vec_t
altar::models::reverso::
operator/(const vec_t & v, double a) {
    return {v[0]/a, v[1]/a, v[2]/a};
}

inline static
altar::models::reverso::mat_t
altar::models::reverso::
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
altar::models::reverso::
norm(const vec_t & v) {
    return std::sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2]);
}

inline static
double
altar::models::reverso::
dot(const vec_t & v1, const vec_t & v2) {
    return v1[0]*v2[0] + v1[1]*v2[1] + v1[2]*v2[2];
}

inline static
altar::models::reverso::vec_t
altar::models::reverso::
cross(const vec_t & v1, const vec_t & v2) {
    return { v1[1]*v2[2] - v1[2]*v2[1], v1[2]*v2[0] - v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0] };
}

inline static
altar::models::reverso::mat_t
altar::models::reverso::
transpose(const mat_t & m) {
    return {m[0], m[3], m[6],
            m[1], m[4], m[7],
            m[2], m[5], m[8]};
};

inline static
altar::models::reverso::vec_t
altar::models::reverso::
xform(const mat_t & m, const vec_t & v) {
    return {m[0]*v[0] + m[1]*v[1] + m[2]*v[2],
            m[3]*v[0] + m[4]*v[1] + m[5]*v[2],
            m[6]*v[0] + m[7]*v[1] + m[8]*v[2]};
};

// end-of-file
