// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 2013-2020 parasim inc
// all rights reserved
//

// externals
#include <cmath>
#include <array>
#include <stdexcept>
#include <gsl/gsl_matrix.h>

// declarations
#include "reverso.h"

// local stuff
namespace altar::models::reverso {

    // constants
    // pi
    const auto pi = 4*std::atan(1.0);

    // types
    using hvec_t = std::array<double, 4>;

    // helper
    auto H(double r2,
           double H_s, double H_d, double a_s, double a_d,
           double gamma_s, double gamma_d,
           double G, double v) -> hvec_t;
}

// the displacement calculator
// definitions
void
altar::models::reverso::
reverso(int sample, const gsl_matrix * locations,
        double H_s, double H_d, double a_s, double a_d, double a_c,
        double Qin,
        double G, double v, double mu, double drho, double g,
        gsl_matrix * predicted)
{
    // initial conditions
    // shallow reservoir overpressure [Pa]
    auto dPs0 = 0.0;
    // deep reservoir overpressure [Pa]
    auto dPd0 = 0.0;

    // ratio of reservoir volumes
    auto k = std::pow(a_d/a_s, 3);
    // length of the hydraulic connection
    auto H_c = H_d - H_s;
    auto gamma_s = 8.0 * (1-v) / (3.0 * pi);
    auto gamma_d = 8.0 * (1-v) / (3.0 * pi);

    auto gamma_r = gamma_s + gamma_d*k;

    // the analytic solution
    // the characteristic time constant (eq. 10)
    auto tau = (8.0 * mu * H_c * gamma_s * gamma_d * k * std::pow(a_s,3))
        / (G * std::pow(a_c,4) * gamma_r);

    auto A  = gamma_d*k / gamma_r;
    A *= dPd0 - dPs0 + drho*g*H_c - 8*gamma_s*mu*Qin*H_c / (pi * std::pow(a_c, 4) * gamma_r);

    // generate the displacements for each observation location
    for (auto loc=0; loc<locations->size1; ++loc) {
        // unpack the observation coordinates
        auto t = gsl_matrix_get(locations, loc, 0);
        auto x = gsl_matrix_get(locations, loc, 1);
        auto y = gsl_matrix_get(locations, loc, 2);
        // compute the pressures
        auto f0 = A * (1. - std::exp(-t/tau));
        auto f1 = G * Qin * t / (pi * std::pow(a_s,3) * gamma_r);

        auto dP_s = dPs0 + f1 + f0;
        auto dP_d = dPd0 + f1 - f0 * gamma_s/(gamma_d*k);

        // compute the square of the distance to the reservoirs
        auto r2 = x*x + y*y;
        // get the H
        auto H_vec = H(r2,
                       H_s, H_d, a_s, a_d, gamma_s, gamma_d,
                       G, v);

        // compute the displacement in the radial direction
        auto u_r = H_vec[0] * dP_s + H_vec[1] * dP_d;
        // compute the displacement in the vertical direction
        auto u_Z = H_vec[2] * dP_s + H_vec[3] * dP_d;

        // find the polar angle of the location
        auto phi = std::atan2(y,x);
        // compute the E and N components
        auto u_E = u_r * std::cos(phi);
        auto u_N = u_r * std::sin(phi);

        // record
        gsl_matrix_set(predicted, sample, 3*loc+0, u_E);
        gsl_matrix_set(predicted, sample, 3*loc+1, u_N);
        gsl_matrix_set(predicted, sample, 3*loc+2, u_Z);

    }

    // all done
    return;
}


// helpers
auto
altar::models::reverso::
H(double r2,
  double H_s, double H_d, double a_s, double a_d,
  double gamma_s, double gamma_d,
  double G, double v) -> hvec_t
{

    auto r = std::sqrt(r2);

    auto H2_s = std::pow(H_s,2);
    auto H2_d = std::pow(H_d,2);

    auto R2_s = r2 + H2_s;
    auto R2_d = r2 + H2_d;

    auto alpha_s = gamma_s == 1.0 ? 1.0 : 4. * H2_s / (pi*R2_s);
    auto alpha_d = gamma_d == 1.0 ? 1.0 : 4. * H2_d / (pi*R2_d);

    auto f_s = std::pow(a_s,3) * alpha_s * (1-v) / (G * std::pow((H2_s+r2),1.5));
    auto f_d = std::pow(a_d,3) * alpha_d * (1-v) / (G * std::pow((H2_d+r2),1.5));

    // make some room
    hvec_t H;

    H[0] = r*f_s;
    H[1] = r*f_d;
    H[2] = H_s*f_s;
    H[3] = H_d*f_d;

    // all done
    return H;
}


// end-of-file
