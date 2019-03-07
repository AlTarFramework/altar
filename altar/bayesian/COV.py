# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2019 parasim inc
# (c) 2010-2019 california institute of technology
# all rights reserved
#


# externals
import itertools
# the package
import altar
# my protocol
from .Scheduler import Scheduler as scheduler


# declaration
class COV(altar.component, family="altar.schedulers.cov", implements=scheduler):
    """
    Annealing schedule based on attaining a particular value for the coefficient of variation
    (COV) of the data likelihood; after Ching[2007].

    The goal is to compute a proposed update Δβ_m to the temperature β_m such that the vector
    of weights w_m given by

        w_m := π(D|θ_m)^{Δβ_m}

    has a particular target value for

        COV(w_m) := <w_m> / \sqrt{<(w_m-<w_m>)^2>}
    """

    # user configurable state
    target = altar.properties.float(default=1.0)
    target.doc = 'the target value for COV'

    tolerance = altar.properties.float(default=.01)
    tolerance.doc = 'the fractional tolerance for achieving the {target} COV value'

    maxiter = altar.properties.int(default=10**3)
    maxiter.doc = 'the maximum number of iterations while looking for a δβ'


    # public data
    w = None # the vector of re-sampling weights
    cov = 0.0 # the actual value for COV we were able to attain


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize me and my parts given an {application} context
        """
        # get the rng wrapper
        rng = application.rng.rng
        # instantiate my COV calculator; {beta.cov} needs the {rng} capsule
        self.minimizer = altar.libaltar.cov(rng.rng, self.maxiter, self.tolerance, self.target)
        # set up the distribution for building the sample multiplicities
        self.uniform = altar.pdf.uniform(support=(0,1), rng=rng)
        # all done
        return self


    @altar.export
    def update(self, step):
        """
        Push {step} forward along the annealing schedule
        """
        # get the new temperature and store it
        β = self.updateTemperature(step=step)
        # compute the new parameter covariance matrix
        Σ = self.computeCovariance(step=step)
        # rank the samples according to their likelihood
        θ, (prior, data, posterior) = self.rank(step=step)

        # update the step
        step.beta = β
        step.theta.copy(θ)
        step.sigma.copy(Σ)
        step.prior.copy(prior)
        step.data.copy(data)
        step.posterior.copy(posterior)

        # and return it
        return step


    @altar.export
    def updateTemperature(self, step):
        """
        Generate the next temperature increment
        """
        # grab the data log-likelihood
        dataLikelihood  = step.data

        # initialize the vector of weights
        self.w = altar.vector(shape=step.samples).zero()
        # compute the median data log-likelihood; clone the source vector first, since the
        # sorting happens in place
        median = dataLikelihood.clone().sort().median()

        # compute {δβ} and the normalized {w}
        β, self.cov = altar.libaltar.dbeta(self.minimizer, dataLikelihood.data, median, self.w.data)

        # and return the new temperature
        return β


    @altar.export
    def computeCovariance(self, step):
        """
        Compute the parameter covariance Σ of the sample in {step}

          Σ = c_m^2 \sum_{i \in samples} \tilde{w}_{i} θ_i θ_i^T} - \bar{θ} \bar{θ}^Τ

        where

          \bar{θ} = \sum_{i \in samples} \tilde{w}_{i} θ_{i}

        The covariance Σ gets used to build a proposal pdf for the posterior
        """
        # unpack what i need
        w = self.w # w is assumed normalized
        θ = step.theta # the current sample set
        # extract the number of samples and number of parameters
        samples = step.samples
        parameters = step.parameters

        # initialize the covariance matrix
        Σ = altar.matrix(shape=(parameters, parameters)).zero()

        # check the geometries
        assert w.shape == samples
        assert θ.shape == (samples, parameters)
        assert Σ.shape == (parameters, parameters)

        # calculate the weighted mean of every parameter across all samples
        θbar = altar.vector(shape=parameters)
        # for each parameter
        for j in range(parameters):
            # the jth column in θ has the value of this parameter in the various samples
            θbar[j] = θ.getColumn(j).mean(weights=w)
        # start filling out Σ
        for i in range(samples):
            # get the sample
            sample = θ.getRow(i)
            # form Σ += w[i] sample sample^T
            altar.blas.dsyr(Σ.lowerTriangular, w[i], sample, Σ)
        # subtract θbar θbar^T
        altar.blas.dsyr(Σ.lowerTriangular, -1, θbar, Σ)
        # fill the upper triangle
        for i in range(parameters):
            for j in range(i):
                Σ[j,i] = Σ[i,j]

        # condition the covariance matrix
        self.conditionCovariance(Σ=Σ)

        # all done
        return Σ


    @altar.export
    def rank(self, step):
        """
        Rebuild the sample and its statistics sorted by the likelihood of the parameter values
        """
        θOld = step.theta
        priorOld = step.prior
        dataOld = step.data
        postOld = step.posterior
        # allocate the new entities
        θ = altar.matrix(shape=θOld.shape)
        prior = altar.vector(shape=priorOld.shape)
        data = altar.vector(shape=dataOld.shape)
        posterior = altar.vector(shape=postOld.shape)

        # build a histogram for the new samples and convert it into a vector
        multi = self.computeSampleMultiplicities(step=step).values()
        # print("      histogram as vector:")
        # print("        counts: {}".format(tuple(multi)))

        # compute the permutation that would sort the frequency table according to the sample
        # multiplicity, in reverse order
        p = multi.sortIndirect().reverse()
        # print("        sorted: {}".format(tuple(p[i] for i in range(p.shape))))

        # the number of samples we have processed
        done = 0
        # start moving stuff around until we have built a complete sample set
        for i in range(p.shape):
            # the old sample index
            old = p[i]
            # and its multiplicity
            count = int(multi[old])
            # if the count has dropped to zero, we are done
            if count == 0: break
            # otherwise, duplicate this sample {count} times
            for dupl in range(count):
                # update the samples
                for param in range(step.parameters):
                    θ[done, param] = θOld[old, param]
                # update the log-likelihoods
                prior[done] = priorOld[old]
                data[done] = dataOld[old]
                posterior[done] = postOld[old]
                # update the number of processed samples
                done += 1
                # print(i, old, count, done)

        # return the shuffled data
        return θ, (prior, data, posterior)


    # implementation details
    def conditionCovariance(self, Σ):
        """
        Make sure the covariance matrix Σ is symmetric and positive definite
        """
        # no need to symmetrize it since it is symmetric by construction
        # NYI: check the eigenvalues to verify positive definiteness
        # all done
        return Σ


    def computeSampleMultiplicities(self, step):
        """
        Prepare a frequency vector for the new samples given the scaled data log-likelihood in
        {w} for this cooling step
        """
        # print("    computing sample multiplicities:")
        # unpack what we need
        w = self.w
        samples = step.samples

        # build a vector of random numbers uniformly distributed in [0,1]
        r = altar.vector(shape=samples).random(pdf=self.uniform)
        # compute the bin edges in the range [0, 1]
        ticks = tuple(self.buildHistogramRanges(w))
        # build a histogram
        h = altar.histogram(bins=samples).ranges(points=ticks).fill(r)
        # and return it
        return h


    def buildHistogramRanges(self, w):
        """
        Build histogram bins based on the scaled data log-likelihood
        """
        # start at 0
        yield 0
        # yield the partial sums
        for partialSum in itertools.accumulate(w): yield partialSum
        # all done
        return


    # private data
    uniform = None
    minimizer = None


# end of file
