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

namespace altar::models::reverso {

    // type definitions
    using vec_t = std::array<double, 3>;
    using mat_t = std::array<double, 9>;
    // constants
    // pi
    const auto pi = 4*std::atan(1.0);
    // machine epsilon
    const auto eps = std::numeric_limits<double>::epsilon();

    // local helpers
    static vec_t
    Urmat(double x, double y, double t,
          const vec_t & b, const vec_t & PA, const vec_t & PB,
          double nu);
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
    // for now, zero out the {predicted} displacements
    gsl_matrix_set_zero(predicted);
    // all done
    return;
}


// end-of-file
