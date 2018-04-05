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

    # user configurable state
    target = altar.properties.float(default=1.0)
    target.doc = 'the target value for COV'

    tolerance = altar.properties.float(default=.01)
    tolerance.doc = 'the fractional tolerance for achieving the {target} COV value'

    maxiter = altar.properties.int(default=10**3)
    maxiter.doc = 'the maximum number of iterations while looking for a δβ'


    # public data
    w = None # the vector of re-sampling weights
    cov = 0.0 # the actual value for COV we were able to attain


    # protocol obligations
    @altar.export
    def initialize(self, controller, model):
        """
        Initialize me and my parts given a {controller} and a {model}
        """
        # get the rng wrapper
        rng = controller.rng.rng
        # instantiate my COV calculator; {beta.cov} needs the {rng} capsule
        self.minimizer = beta.cov(rng.rng, self.maxiter, self.tolerance, self.target)
        # set up the distribution for building the sample multiplicities
        self.uniform = altar.pdf.uniform(support=(0,1), rng=rng)
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


    # private data
    uniform = None
    minimizer = None


# end of file
