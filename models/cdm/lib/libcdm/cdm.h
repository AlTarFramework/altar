// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// parasim
// (c) 2013-2019 all rights reserved
//

// code guard
#if !defined(altar_models_cdm_cdm_h)
#define altar_models_cdm_cdm_h

namespace altar {
    namespace models {
        namespace cdm {
            void cdm(const gsl_matrix * locations,
                     double X0, double Y0, double depth,
                     double ax, double ay, double az,
                     double omegaX, double omegaY, double omegaZ,
                     double opening,
                     double nu,
                     gsl_matrix * predicted
                     );
        }
    }
}

#endif

// end of file
