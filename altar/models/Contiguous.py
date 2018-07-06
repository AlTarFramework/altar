# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# the package
import altar
# the protocol
from .ParameterSet import ParameterSet as parameters


# component
class Contiguous(altar.component,
                 family="altar.models.parameters.contiguous", implements=parameters):
    """
    A contiguous parameter set
    """


    # user configurable state
    count = altar.properties.int(default=1)
    count.doc = "the number of parameters in this set"

    prior = altar.distributions.distribution()
    prior.doc = "the prior distribution"

    prep = altar.distributions.distribution()
    prep.doc = "the distribution to use to initialize this parameter set"


    # state set by the model
    offset = 0 # adjusted by the model after the full set of parameters is known


# end of file
