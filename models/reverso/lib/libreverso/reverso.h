// -*- C++ -*-
//
// eric m. gurrola <eric.m.gurrola@jpl.nasa.gov>
//
// (c) 2019 jet propulsion laboratory
// california institute of technology
// all rights reserved
//

// code guard
#if !defined(altar_models_cdm_cdm_h)
#define altar_models_cdm_cdm_h

namespace altar {
    namespace models {
        namespace reverso {
            void reverso(int sample,
                     const gsl_matrix * locations, const gsl_matrix * los,
                     double g, double Gsm, double nu, double mu, double drho,
                     double x0, double y0, double t0,
                     double as, double ac, double ad,
                     double hs, double hd, double qin,
                     gsl_matrix * predicted
                     );
        }
    }
}

#endif

// end of file
