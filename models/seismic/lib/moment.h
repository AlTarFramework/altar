// -*- C++ -*-
//
// Lijun Zhu
// Caltech
// (c) 1998-2018 all rights reserved
//


#include <gsl/vector.h>
#include <gsl/matrix.h>


#ifndef __altar_seismic_moment_h
#define __altar_seismic_moment_h

namespace altar {
    namespace seismic {
        namespace moment {
            double sample(double Mw_mean, double Mw_sigma, int nPatches);
            double density(double x, double Mw_mean, double Mw_sigma, int nPatches);
            void vector(gsl_vector * v, gsl_rng * rng, double Mw_mean, double Mw_sigma, int nPatches);
            void matrix(gsl_matrix * m, gsl_rng * rng, double Mw_mean, double Mw_sigma, int nPatches);
        }
    }
}

#endif //__altar_seismic_moment_h
