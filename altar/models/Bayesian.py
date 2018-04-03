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
    controller = altar.bayesian.controller()
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
        return self.controller.posterior(model=self)


    # implementation details
    def initialize(self, app):
        """
        Initialize the state of the model given a {problem} specification
        """
        # get the job parameters
        self.job = app.job
        # grab the journal channels
        self.info = app.info
        self.warning = app.warning
        self.error = app.error
        self.debug = app.debug
        self.firewall = app.firewall

        # initialize my controller
        self.controller.initialize(model=self)

        # all done
        return self


    # public data
    # job parameters
    job = None
    # journal channels
    info = None
    warning = None
    error = None
    default = None
    firewall = None


# end of file
