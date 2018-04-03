# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# get the package
import altar


# the scheduler protocol
class Scheduler(altar.protocol, family="altar.schedulers"):
    """
    The protocol that all AlTar schedulers must implement
    """

    # required behavior
    @altar.provides
    def initialize(self, model):
        """
        Initialize me and my parts given a {model}
        """

    @altar.provides
    def update(self, coolingStep):
        """
        Push {coolingStep} forward along the annealing schedule
        """

    @altar.provides
    def updateTemperature(self, coolingStep):
        """
        Generate the next temperature increment
        """

    @altar.provides
    def computeCovariance(self, coolingStep):
        """
        Compute the parameter covariance of the sample in the {coolingStep}
        """

    @altar.provides
    def rank(self, coolingStep):
        """
        Rebuild the sample and its statistics sorted by the likelihood of the parameter values
        """


    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # by default, we do CATMIP as encapsulated by the {Annealer} class
        from .Annealer import Annealer as default
        # and return it
        return default


# end of file
