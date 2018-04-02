# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# my base class
from .Bayesian import Bayesian


# declaration
class Null(Bayesian, family="altar.models.null"):
    """
    A trivial model that can be used as a base class for deriving interesting ones
    """


# end of file
