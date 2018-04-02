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
from .Model import Model as model


# declaration
class Bayesian(altar.component, family="altar.models.bayesian", implements=model):
    """
    The base class of AlTar models that are compatible with Bayesian explorations
    """


    # user configurable state
    controller = altar.mcmc.controller()
    controller.doc = "my simulation controller"


    # protocol obligations
    @altar.export
    def posterior(self, app):
        """
        Sample my posterior distribution
        """
        # initialize my parts
        self.initialize(app=app)
        # ask my controller to help me sample my posterior distribution
        self.controller.posterior(model=self)
        # all done
        return


    # implementation details
    def initialize(self, app):
        """
        Initialize the state of the model given a {problem} specification
        """
        # and my controller
        self.controller.initialize(model=self)
        # all done
        return


# end of file
