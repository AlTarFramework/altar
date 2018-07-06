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


# the parameter set protocol
class ParameterSet(altar.protocol, family="altar.models.parameters"):
    """
    The protocol that all AlTar parameter sets must implement
    """


    # required state
    count = altar.properties.int(default=1)
    count.doc = "the number of parameters in this set"

    prior = altar.distributions.distribution()
    prior.doc = "the prior distribution"

    prep = altar.distributions.distribution()
    prep.doc = "the distribution to use to initialize this parameter set"


# end of file
