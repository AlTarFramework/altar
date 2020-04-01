# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis (michael.aivazis@para-sim.com)
# grace bato           (mary.grace.p.bato@jpl.nasa.gov)
# eric m. gurrola      (eric.m.gurrola@jpl.nasa.gov)
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved


# framework
import altar
# the fast displacement calculator
from altar.models.reverso.ext import libreverso


# the strategy
class Fast:
    """
    A strategy for computing displacements predicted by the Reverso model that is implemented
    in C++
    """


    # interface
    def initialize(self, model, **kwds):
        """
        Initialize the strategy with {model} information
        """
        # build the calculator and attach it
        self.source = source = libreverso.newSource(model.G, model.v, model.mu, model.drho, model.g)

        # get the locations and time of the observations
        ticks = model.ticks
        # the observed displacements
        displacements = model.d

        # attach the coordinates of the observation points
        libreverso.locations(source, ticks)
        # and the observations
        libreverso.data(source, displacements.data)
        # inform the source about the sample layout; assume contiguous parameter sets
        libreverso.layout(source,
                          model.Qin_idx,
                          model.Hs_idx, model.Hd_idx, model.as_idx, model.ad_idx, model.ac_idx)

        # all done
        return self


    def dataLikelihood(self, model, step):
        """
        Fill {step.data} with the likelihood of the samples in {step.theta} given the available
        data
        """
        # grab my calculator
        source = self.source
        # compute the portion of the sample that belongs to me
        θ = model.restrict(theta=step.theta)
        # allocate a matrix to hold the predicted displacements
        predicted = altar.matrix(shape=(step.samples, 3*model.observations))

        # compute the predicted displacements
        libreverso.displacements(source, θ.capsule, predicted.data)
        # compute the residuals (in place)
        libreverso.residuals(source, predicted.data)

        # get the norm
        norm = model.norm
        # the inverse of the covariance matrix
        cd_inv = model.cd_inv
        # the normalization
        normalization = model.normalization
        # and the data likelihood vector
        dataLLK = step.data

        # find out how many samples in the set
        samples = θ.rows
        # go through the samples
        for sample in range(samples):
            # get the residuals
            residuals = predicted.getRow(sample)
            # compute the norm
            nrm = norm.eval(v=residuals, sigma_inv=cd_inv)
            # and normalize it
            llk = normalization - nrm**2 / 2
            # and store it
            dataLLK[sample] = llk

        # all done
        return self


    # private data
    source = None


# end of file
