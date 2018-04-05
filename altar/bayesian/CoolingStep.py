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


# declaration
class CoolingStep:
    """
    Encapsulation of the state of the calculation at some particular β value
    """


    # public data
    beta = None      # the inverse temperature
    theta = None     # a (samples x parameters) matrix
    prior = None     # a (samples) vector with logs of the sample likelihoods
    data = None      # a (samples) vector with the logs of the data likelihoods given the samples
    posterior = None # a (samples) vector with the logs of the posterior likelihood

    sigma = None # the parameter covariance matrix


    # read-only public data
    @property
    def samples(self):
        """
        The number of samples
        """
        # encoded in θ
        return self.theta.rows


    @property
    def parameters(self):
        """
        The number of model parameters
        """
        # encoded in θ
        return self.theta.columns


    # factories
    @classmethod
    def start(cls, model):
        """
        Build the first cooling step by asking {model} to produce a sample set from its
        initializing prior, compute the likelihood of this sample given the data, and compute a
        (perhaps trivial) posterior
        """
        # build an uninitialized step
        step = cls.alloc(samples=model.job.chains, parameters=model.parameters())

        # initialize it
        model.sample(step=step)
        # compute the likelihoods
        model.likelihoods(step=step)

        # return the initialized state
        return step


    @classmethod
    def alloc(cls, samples, parameters):
        """
        Allocate storage for the parts of a cooling step
        """
        # allocate the initial sample set
        theta = altar.matrix(shape=(samples, parameters))
        # allocate the likelihood vectors
        prior = altar.vector(shape=samples)
        data = altar.vector(shape=samples)
        posterior = altar.vector(shape=samples)
        # build one of my instances and return it
        return cls(beta=0, theta=theta, likelihoods=(prior, data, posterior))


    # interface
    def clone(self):
        """
        Make a new step with a duplicate of my state
        """
        # make copies of my state
        beta = self.beta
        theta = self.theta.clone()
        sigma = self.sigma.clone()
        likelihoods = self.prior.clone(), self.data.clone(), self.posterior.clone()

        # make one and return it
        return type(self)(beta=beta, theta=theta, likelihoods=likelihoods, sigma=sigma)


    # meta-methods
    def __init__(self, beta, theta, likelihoods, sigma=None, **kwds):
        # chain up
        super().__init__(**kwds)

        # store the temperature
        self.beta = beta
        # store the sample set
        self.theta = theta
        # store the likelihoods
        self.prior, self.data, self.posterior = likelihoods

        # get the number of parameters
        dof = self.parameters
        # initialize the covariance matrix
        self.sigma = altar.matrix(shape=(dof,dof)).zero() if sigma is None else sigma

        # all done
        return


# end of file
