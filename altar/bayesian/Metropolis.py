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
import math
# the package
import altar
# my protocol
from .Sampler import Sampler as sampler


# declaration
class Metropolis(altar.component, family="altar.samplers.metropolis", implements=sampler):
    """
    The Metropolis algorithm as a sampler of the posterior distribution
    """


    # types
    from .CoolingStep import CoolingStep


    # user configurable state
    steps = altar.properties.int(default=20)
    steps.doc = 'the length of each Markov chain'

    scaling = altar.properties.float(default=.1)
    scaling.doc = 'the parameter covariance Σ is scaled by the square of this'

    acceptanceWeight = altar.properties.float(default=8)
    acceptanceWeight.doc = 'the weight of accepted samples during covariance rescaling'

    rejectionWeight = altar.properties.float(default=1)
    rejectionWeight.doc = 'the weight of rejected samples during covariance rescaling'


    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        Initialize me and my parts given a {model}
        """
        # get the capsule of the random number generator
        rng = application.rng.rng
        # set up the distribution for building the sample multiplicities
        self.uniform = altar.pdf.uniform(support=(0,1), rng=rng)
        # set up the distribution for the random walk displacement vectors
        self.uninormal = altar.pdf.ugaussian(rng=rng)

        # all done
        return self


    @altar.export
    def samplePosterior(self, annealer, step):
        """
        Sample the posterior distribution
        """
        # prepare the sampling pdf
        self.prepareSamplingPDF(step=step)
        # walk the chains
        statistics = self.walkChains(model=annealer.model, step=step)
        # all done
        return statistics


    @altar.provides
    def equilibrate(self, annealer, statistics):
        """
        Update my statistics based on the results of walking my Markov chains
        """
        # update the scaling of the parameter covariance matrix
        self.adjustCovarianceScaling(*statistics)
        # all done
        return


    # implementation details
    def prepareSamplingPDF(self, step):
        """
        Re-scale and decompose the parameter covariance matrix, in preparation for the
        Metropolis update
        """
        # unpack what i need
        Σ = step.sigma.clone()
        # scale it
        Σ *= self.scaling**2
        # compute its Cholesky decomposition
        self.sigma_chol = altar.lapack.cholesky_decomposition(Σ)
        # all done
        return


    def walkChains(self, model, step):
        """
        Run the Metropolis algorithm on the Markov chains
        """
        # unpack what i need from the cooling step
        β = step.beta
        θ = step.theta
        prior = step.prior
        data = step.data
        posterior = step.posterior
        # get the parameter covariance
        Σ_chol = self.sigma_chol
        # the sample geometry
        samples = step.samples
        parameters = step.parameters
        # a couple of functions from the math module
        exp = math.exp
        log = math.log

        # reset the accept/reject counters
        accepted = rejected = unlikely = 0

        # allocate some vectors that we use throughout the following
        # candidate likelihoods
        cprior = altar.vector(shape=samples)
        cdata = altar.vector(shape=samples)
        cpost = altar.vector(shape=samples)
        # a fake covariance matrix for the candidate steps, just so we don't have to rebuild it
        # every time
        csigma = altar.matrix(shape=(parameters,parameters))
        # the mask of samples rejected due to model constraint violations
        rejects = altar.vector(shape=samples)
        # and a vector with random numbers for the Metropolis acceptance
        dice = altar.vector(shape=samples)

        # step all chains together
        for step in range(self.steps):
            # initialize the candidate sample by randomly displacing the current one
            cθ = self.displace(sample=θ)
            # initialize the likelihoods
            likelihoods = cprior.zero(), cdata.zero(), cpost.zero()
            # and the covariance matrix
            csigma.zero()
            # build a candidate state
            candidate = self.CoolingStep(beta=β, theta=cθ,
                                         likelihoods=likelihoods, sigma=csigma)
            # the random displacement may have generated candidates that are outside the
            # support of the model, so we must give it an opportunity to reject them;
            # reset the mask and ask the model to verify the sample validity
            rejects = model.verify(step=candidate, mask=rejects.zero())
            # make the candidate a consistent set by replacing the rejected samples with copies
            # of the originals from {θ}
            for index, flag in enumerate(rejects):
                # if this sample was rejected
                if flag:
                    # copy the corresponding row from {θ} into {candidate}
                    cθ.setRow(index, θ.getRow(index))

            # compute the likelihoods
            model.likelihoods(candidate)

            # build a vector to hold the difference of the two posterior likelihoods
            diff = cpost.clone()
            # subtract the previous posterior
            diff -= posterior
            # randomize the Metropolis acceptance vector
            dice.random(self.uniform)

            # accept/reject: go through all the samples
            for sample in range(samples):
                # a candidate is rejected if the model considered it invalid
                if rejects[sample]:
                    # nothing to do: θ, priorL, dataL, and postL contain the right statistics
                    # for this sample; just update the rejection count
                    rejected += 1
                    # and move on
                    continue
                # a candidate is also rejected if the model considered it less likely than the
                # original and it wasn't saved by the {dice}
                if log(dice[sample]) > diff[sample]:
                    # nothing to do: θ, priorL, dataL, and postL contain the right statistics
                    # for this sample; just update the unlikely count
                    unlikely += 1
                    # and move on
                    continue

                # otherwise, update the acceptance count
                accepted += 1
                # copy the candidate sample
                θ.setRow(sample, cθ.getRow(sample))
                # and its likelihoods
                prior[sample] = cprior[sample]
                data[sample] = cdata[sample]
                posterior[sample] = cpost[sample]

        # all done
        return accepted, rejected, unlikely


    def displace(self, sample):
        """
        Construct a set of displacement vectors for the random walk from a distribution with zero
        mean and my covariance
        """
        # get my decomposed covariance
        Σ_chol = self.sigma_chol

        # build a set of random displacement vectors; note that, for convenience, this starts
        # out as (parameters x samples), i.e. the transpose of what we need
        δT = altar.matrix(shape=tuple(reversed(sample.shape))).random(pdf=self.uninormal)
        # multiply the displacement vectors by the decomposed covariance
        δT = altar.blas.dtrmm(
            Σ_chol.sideLeft, Σ_chol.lowerTriangular, Σ_chol.opNoTrans, Σ_chol.nonUnitDiagonal,
            1, Σ_chol, δT)

        # allocate the transpose
        δ = altar.matrix(shape=sample.shape)
        # fill it
        δT.transpose(δ)
        # offset it by the original sample
        δ += sample
        # and return it
        return δ


    def adjustCovarianceScaling(self, accepted, rejected, unlikely):
        """
        Compute a new value for the covariance sacling factor based on the acceptance/rejection
        ratio
        """
        # unpack my weights
        aw = self.acceptanceWeight
        rw = self.rejectionWeight
        # compute the acceptance ratio
        acceptance = accepted / (accepted + rejected + unlikely)
        # the fudge factor
        kc = (aw*acceptance + rw)/(aw+rw)
        # don't let it get too small
        if kc < .1: kc = .1
        # or too big
        if kc > 1.: kc = 1.
        # store it
        self.scaling = kc
        # and return
        return self


    # public data
    uniform = None
    uninormal = None
    sigma_chol = None


# end of file
