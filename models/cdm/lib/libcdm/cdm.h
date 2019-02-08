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
            void cdm(double X, double Y,
                     double X0, double Y0, double depth,
                     double omegaX, double omegaY, double omegaZ,
                     double ax, double ay, double az,
                     double opening,
                     double nu);
        }
    }
}

#endif

// end of file
