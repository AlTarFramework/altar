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
from .Controller import Controller as controller


# my declaration
class Annealer(altar.component, family="altar.controllers.annealer", implements=controller):
    """
    A Bayesian controller that uses an annealing schedule and MCMC to approximate the posterior
    distribution of a model
    """


    # protocol obligations
    @altar.export
    def posterior(self, model):
        """
        Sample the posterior distribution
        """
        print(f"controller: {self}")
        print(f"  model: {model}")
        # all done
        return


    @altar.export
    def initialize(self, model):
        """
        Initialize me and my parts given a {model}
        """
        # all done
        return


# end of file
