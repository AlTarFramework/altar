// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// parasim
// (c) 2013-2020 all rights reserved
//

// code guard
#if !defined(altar_models_reverso_reverso_h)
#define altar_models_reverso_reverso_h

namespace altar::models::reverso {
    void reverso(int sample, const gsl_matrix * locations,
                 double H_s, double H_d, double a_s, double a_d, double a_c,
                 double _Qin,
                 double G, double v, double mu, double drho, double g,
                 gsl_matrix * predicted);
}

#endif

// end of file
