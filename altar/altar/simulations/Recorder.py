# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#


# the package
import altar
# my protocol
from .Archiver import Archiver as archiver


# an implementation of the archiver protocol
class Recorder(altar.component, family="altar.simulations.archivers.recorder", implements=archiver):
    """
    Recorder stores the intermediate simulation state in memory
    """


    # user configurable state
    theta = altar.properties.path(default="theta.txt")
    theta.doc = "the path to the file with the final posterior sample"

    sigma = altar.properties.path(default="sigma.txt")
    sigma.doc = "the path to the file with the final parameter correlation matrix"

    llk = altar.properties.path(default="llk.txt")
    llk.doc = "the path to the file with the final posterior log likelihood"


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize me given an {application} context
        """
        # all done
        return self


    @altar.export
    def record(self, step, **kwds):
        """
        Record the final state of the calculation
        """
        # record the samples
        step.theta.save(filename=self.theta)
        # the covariance matrix
        step.sigma.save(filename=self.sigma)
        # and the posterior log likelihood
        step.posterior.save(filename=self.llk)
        # all done
        return self


# end of file
