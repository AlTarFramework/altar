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
    prior = None     # a (samples) vector with logs of the sample densities
    data = None      # a (samples) vector with the logs of the data densities given the samples
    posterior = None # a (samples) vector with the logs of the posterior likelihood

    sigma = None # the parameter covariance matrix

    iteration = 0 # the sequence number of annealing step; assigned as worker.iteration

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
    def start(cls, annealer):
        """
        Build the first cooling step by asking {model} to produce a sample set from its
        initializing prior, compute the likelihood of this sample given the data, and compute a
        (perhaps trivial) posterior
        """
        # get the model
        model = annealer.model
        # build an uninitialized step
        step = cls.alloc(samples=model.job.chains, parameters=model.parameters)

        # initialize it
        model.initializeSample(step=step)
        # compute the densities
        model.densities(annealer=annealer, step=step)

        # return the initialized state
        return step


    @classmethod
    def alloc(cls, samples, parameters):
        """
        Allocate storage for the parts of a cooling step
        """
        # allocate the initial sample set
        theta = altar.matrix(shape=(samples, parameters)).zero()
        # allocate the likelihood vectors
        prior = altar.vector(shape=samples).zero()
        data = altar.vector(shape=samples).zero()
        posterior = altar.vector(shape=samples).zero()
        # build one of my instances and return it
        return cls(beta=0, theta=theta, densities=(prior, data, posterior))


    # interface
    def clone(self):
        """
        Make a new step with a duplicate of my state
        """
        # make copies of my state
        beta = self.beta
        theta = self.theta.clone()
        sigma = self.sigma.clone()
        densities = self.prior.clone(), self.data.clone(), self.posterior.clone()

        # make one and return it
        return type(self)(beta=beta, theta=theta, densities=densities, sigma=sigma)


    # meta-methods
    def __init__(self, beta, theta, densities, sigma=None, **kwds):
        # chain up
        super().__init__(**kwds)

        # store the temperature
        self.beta = beta
        # store the sample set
        self.theta = theta
        # store the densities
        self.prior, self.data, self.posterior = densities

        # get the number of parameters
        dof = self.parameters
        # initialize the covariance matrix
        self.sigma = altar.matrix(shape=(dof,dof)).zero() if sigma is None else sigma

        # all done
        return


    # implementation details
    def print(self, channel, indent=' '*2):
        """
        Print info about this step
        """
        # unpack my shape
        samples = self.samples
        parameters = self.parameters

        # say something
        channel.line(f"step")
        # show me the temperature
        channel.line(f"{indent}β: {self.beta}")
        # the sample
        θ = self.theta
        channel.line(f"{indent}θ: ({θ.rows} samples) x ({θ.columns} parameters)")

        if θ.rows <= 10 and θ.columns <= 10:
            channel.line("\n".join(θ.print(interactive=False, indent=indent*2)))
            
        if samples < 10:
            # the prior
            prior = self.prior
            channel.line(f"{indent}prior:")
            channel.line(prior.print(interactive=False, indent=indent*2))
            # the data
            data = self.data
            channel.line(f"{indent}data:")
            channel.line(data.print(interactive=False, indent=indent*2))
            # the posterior
            posterior = self.posterior
            channel.line(f"{indent}posterior:")
            channel.line(posterior.print(interactive=False, indent=indent*2))

        if parameters < 10:            
            # the data covariance
            Σ = self.sigma
            channel.line(f"{indent}Σ: {Σ.rows} x {Σ.columns}")
            channel.line("\n".join(Σ.print(interactive=False, indent=indent*2)))

        # the statistics of parameters
        mean, sd = altar.stats.mean_sd(θ)
        channel.line(f"{indent}parameters (mean, sd):")
        for i in range(min(100, parameters)):
            channel.line(f"{indent} ({mean[i]}, {sd[i]})")

        # flush
        channel.log()

        # all done
        return channel


# end of file
