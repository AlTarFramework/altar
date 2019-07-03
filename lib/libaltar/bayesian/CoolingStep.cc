// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2019 parasim inc
// (c) 2010-2019 california institute of technology
// all rights reserved
//


// for the build system
#include <portinfo>

// get my declarations
#include "CoolingStep.h"


// meta-methods
// destructor
altar::bayesian::CoolingStep::
~CoolingStep()
{
    // release the gsl entities
    gsl_matrix_free(_theta);
    gsl_vector_free(_prior);
    gsl_vector_free(_data);
    gsl_vector_free(_posterior);
    gsl_matrix_free(_sigma);
}


// end of file
