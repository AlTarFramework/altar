# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
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
    def initialize(self, application):
        """
        Initialize me and my parts given an {application} context
        """

    @altar.provides
    def update(self, step):
        """
        Push {step} forward along the annealing schedule
        """

    @altar.provides
    def updateTemperature(self, step):
        """
        Generate the next temperature increment
        """

    @altar.provides
    def computeCovariance(self, step):
        """
        Compute the parameter covariance of the sample in the {step}
        """

    @altar.provides
    def rank(self, step):
        """
        Rebuild the sample and its statistics sorted by the likelihood of the parameter values
        """

    # framework hooks
    @classmethod
    def pyre_default(cls, **kwds):
        """
        Supply a default implementation
        """
        # by default, use COV
        from .COV import COV as default
        # and return it
        return default

# end of file
