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
# my base class
from .Bayesian import Bayesian


# declaration
class Null(Bayesian, family="altar.models.null"):
    """
    A trivial model that can be used as a base class for deriving interesting ones
    """


    @altar.export
    def parameters(self):
        """
        The number of parameters in the 'null' model
        """
        # make something up
        return 1


# end of file
