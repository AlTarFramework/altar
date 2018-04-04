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
# my protocol
from .Scheduler import Scheduler as scheduler


# declaration
class COV(altar.component, family="altar.schedulers.cov", implements=scheduler):
    """
    Annealing schedule based on attaining a particular value for the coefficient of variation
    (COV) of the data likelihood; after Ching[2007].

    The goal is to compute a proposed update Δβ_m to the temperature β_m such that the vector
    of weights w_m given by

        w_m := π(D|θ_m)^{Δβ_m}

    has a particular target value for

        COV(w_m) := <w_m> / \sqrt{<(w_m-<w_m>)^2>}
    """

    # protocol obligations
    @altar.export
    def initialize(self, model):
        """
        Initialize me and my parts given a {model}
        """
        # all done
        return self


    @altar.export
    def update(self, step):
        """
        Push {step} forward along the annealing schedule
        """
        # all done
        return self


    @altar.export
    def updateTemperature(self, step):
        """
        Generate the next temperature increment
        """
        # all done
        return self


    @altar.export
    def computeCovariance(self, step):
        """
        Compute the parameter covariance of the sample in the {step}
        """
        # all done
        return self


    @altar.export
    def rank(self, step):
        """
        Rebuild the sample and its statistics sorted by the likelihood of the parameter values
        """
        # all done
        return self


# end of file
