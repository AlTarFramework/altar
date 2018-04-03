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


    @altar.export
    def update(self, coolingStep):
        """
        Push {coolingStep} forward along the annealing schedule
        """


    @altar.export
    def updateTemperature(self, coolingStep):
        """
        Generate the next temperature increment
        """


    @altar.export
    def computeCovariance(self, coolingStep):
        """
        Compute the parameter covariance of the sample in the {coolingStep}
        """


    @altar.export
    def rank(self, coolingStep):
        """
        Rebuild the sample and its statistics sorted by the likelihood of the parameter values
        """


# end of file
