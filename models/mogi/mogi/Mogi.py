# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# externals
from math import sqrt, π
# the package
import altar


# declaration
class Mogi(altar.models.bayesian, family="altar.models.mogi"):
    """
    An implementation of Mogi[1958]

    The surface displacement calculation for a point pressure source in an elastic half space.

    This is a four parameter model: x,y,depth to locate the point source, and the volume change
    """


    # user configurable state
    parameters = altar.properties.int(default=4)
    parameters.doc = "the number of model degrees of freedom"

    prep = altar.distributions.distribution()
    prep.doc = "the distribution used to generate the initial sample"

    prior = altar.distributions.distribution()
    prior.doc = "the prior distribution"

    # model specific parameters
    depth = altar.properties.array(default=[0, 60000]) # in SI
    depth.doc = "the allowed range for the depth parameter"

    # observations
    stations = altar.properties.istream(default="stations.csv")
    stations.doc = "the name of the file with the locations of the observation points"


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize the state of the model given a {problem} specification
        """
        # chain up
        super().initialize(application=application)
        # get my random number generator
        rng = self.rng

        # initialize my distributions
        self.prep.initialize(rng=rng)
        self.prior.initialize(rng=rng)

        # all done
        return self


    @altar.export
    def initializeSample(self, step):
        """
        Fill {step.θ} with an initial random sample from my prior distribution.
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # fill it with random numbers from my initializer
        self.prep.initializeSample(theta=θ)
        # and return
        return self


    @altar.export
    def priorLikelihood(self, step):
        """
        Fill {step.prior} with the likelihoods of the samples in {step.theta} in the prior
        distribution
        """
        # grab my prior pdf
        pdf = self.prior
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # and the storage for the prior likelihoods
        likelihood = step.prior

        # delegate
        pdf.priorLikelihood(theta=θ, likelihood=likelihood)

        # all done
        return self


    @altar.export
    def dataLikelihood(self, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data. This is what is usually referred to as the "forward model"
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # and the storage for the data likelihoods
        data = step.data

        # find out how many samples in the set
        samples = θ.rows

        # for each sample in the sample set
        for sample in range(samples):
            # compute the expected displacement
            u = self.mogi(parameters=θ[sample])
            # how likely is it given my observations
            raise NotImplementedError("NYI: compare with observations")

            # data[sample] = log likelihood of this (predicted, expected) pair

        # all done
        return self


    @altar.export
    def verify(self, step, mask):
        """
        Check whether the samples in {step.theta} are consistent with the model requirements and
        update the {mask}, a vector with zeroes for valid samples and non-zero for invalid ones
        """
        # grab the portion of the sample that's mine
        θ = self.restrict(theta=step.theta)
        # grab my prior
        pdf = self.prior
        # ask it to verify my samples
        pdf.verify(theta=θ, mask=mask)
        # all done; return the rejection map
        return mask


    # meta methods
    def __init__(self, **kwds):
        # chain up
        super().__init__(**kwds)
        # all done
        return


    # implementation details
    def mogi(self, parameters):
        """
        Compute the expected displacements from a point pressure source at the set of observation
        locations
        """
        # unpack the parameters
        x_source = parameters[0]
        y_source = parameters[1]
        d_source = parameters[2]
        dV = parameters[3]

        # get the list of locations of interest
        locations = self.locations

        # allocate space for the result
        u = altar.matrix(shape=(len(locations), 3))
        # go through each observation location
        for index, (x_obs,y_obs) in enumerate(self.locations):
            #
            x = x_source - x_obs
            y = y_source - y_obs
            # compute the distance to the point source
            x2 = x**2
            y2 = y**2
            d2 = (d_source)**2
            # intermediate values
            C = (nu-1)*dV/π
            R = sqrt(x2+y2+d2)
            R3 = C*R**-3
            # store the expected displacement
            u[index,0], u[index,1], u[index,2] = x*R3, y*R3, -d_source*R3

        # all done
        return u

# end of file
