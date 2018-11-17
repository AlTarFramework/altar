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
        Initialize me and my parts given an {application} context
        """
        # pull the chain length from the job specification
        self.steps = application.job.steps
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
        # grab the dispatcher
        dispatcher = annealer.dispatcher
        # notify we have started sampling the posterior
        dispatcher.notify(event=dispatcher.samplePosteriorStart, controller=annealer)
        # prepare the sampling pdf
        self.prepareSamplingPDF(annealer=annealer, step=step)
        # walk the chains
        statistics = self.walkChains(annealer=annealer, step=step)
        # notify we are done sampling the posterior
        dispatcher.notify(event=dispatcher.samplePosteriorFinish, controller=annealer)
        # all done
        return statistics


    @altar.provides
    def resample(self, annealer, statistics):
        """
        Update my statistics based on the results of walking my Markov chains
        """
        # update the scaling of the parameter covariance matrix
        self.adjustCovarianceScaling(*statistics)
        # all done
        return


    # implementation details
    def prepareSamplingPDF(self, annealer, step):
        """
        Re-scale and decompose the parameter covariance matrix, in preparation for the
        Metropolis update
        """
        # get the dispatcher
        dispatcher = annealer.dispatcher
        # notify we have started preparing the sampling PDF
        dispatcher.notify(event=dispatcher.prepareSamplingPDFStart, controller=annealer)
        # unpack what i need
        Σ = step.sigma.clone()
        # scale it
        Σ *= self.scaling**2
        # compute its Cholesky decomposition
        self.sigma_chol = altar.lapack.cholesky_decomposition(Σ)
        # notify we are done preparing the sampling PDF
        dispatcher.notify(event=dispatcher.prepareSamplingPDFFinish, controller=annealer)
        # all done
        return


    def walkChains(self, annealer, step):
        """
        Run the Metropolis algorithm on the Markov chains
        """
        # get the model
        model = annealer.model
        # and the event dispatcher
        dispatcher = annealer.dispatcher

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
            # notify we are advancing the chains
            dispatcher.notify(event=dispatcher.chainAdvanceStart, controller=annealer)

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
            # notify we are starting the verification process
            dispatcher.notify(event=dispatcher.verifyStart, controller=annealer)
            # reset the mask and ask the model to verify the sample validity
            model.verify(step=candidate, mask=rejects.zero())
            # make the candidate a consistent set by replacing the rejected samples with copies
            # of the originals from {θ}
            for index, flag in enumerate(rejects):
                # if this sample was rejected
                if flag:
                    # copy the corresponding row from {θ} into {candidate}
                    cθ.setRow(index, θ.getRow(index))
            # notify that the verification process is finished
            dispatcher.notify(event=dispatcher.verifyFinish, controller=annealer)

            # compute the likelihoods
            model.likelihoods(annealer=annealer, step=candidate)

            # build a vector to hold the difference of the two posterior likelihoods
            diff = cpost.clone()
            # subtract the previous posterior
            diff -= posterior
            # randomize the Metropolis acceptance vector
            dice.random(self.uniform)

            # notify we are starting accepting samples
            dispatcher.notify(event=dispatcher.acceptStart, controller=annealer)

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

            # notify we are done accepting samples
            dispatcher.notify(event=dispatcher.acceptFinish, controller=annealer)

            # notify we are done advancing the chains
            dispatcher.notify(event=dispatcher.chainAdvanceFinish, controller=annealer)


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


    # private data
    steps = 1          # the length of each Markov chain

    uniform = None     # the distribution of the sample multiplicities
    uninormal = None   # the distribution of random walk displacement vectors
    sigma_chol = None  # placeholder for the scaled and decomposed parameter covariance matrix

    dispatcher = None  # a reference to the event dispatcher


# end of file
