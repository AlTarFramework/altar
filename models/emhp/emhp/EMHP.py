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


# declaration
class EMHP(altar.models.bayesian, family="altar.models.emhp"):
    """
    A diagnostic tool
    """


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given a {problem} specification
        """
        # chain up
        super().initialize(application=application)
        # all done
        return self


    # services
    @altar.export
    def initializeSample(self, step):
        """
        File {step.theta} with an initial random sample form my prior distribution
        """
        # all done
        return self


    @altar.export
    def priorLikelihood(self, step):
        """
        Fill {step.prior} with the likelihoods of the samples in {step.theta} in the prior
        distribution
        """
        # all done
        return self


    @altar.export
    def dataLikelihood(self, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """
        # all done
        return self


    @altar.export
    def verify(self, step, mask):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        update the {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # all done; return the rejection map
        return mask


# end of file
