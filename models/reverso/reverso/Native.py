# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis (michael.aivazis@para-sim.com)
# grace bato           (mary.grace.p.bato@jpl.nasa.gov)
# eric m. gurrola      (eric.m.gurrola@jpl.nasa.gov)
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved


# externals
import math
# the framework
import altar
# the pure python implementation of the CDM source
from .Source import Source as source


# declaration
class Native:
    """
    A strategy for computing the data log likelihood that is written in pure python
    """

    # interface
    def initialize(self, **kwds):
        """
        Initialize the strategy
        """
        # nothing to do
        return self


    def dataLikelihood(self, model, step):
        """
        Fill {step.data} with the likelihoods of the samples in {step.theta} given the available
        data.
        """
        # get the norm
        norm = model.norm
        # grab the portion of the sample that belongs to this model
        θ = model.restrict(theta=step.theta)
        # the observed displacements
        displacements = model.d
        # the inverse of the data covariance matrix
        cd_inv = model.cd_inv
        # the normalization
        normalization = model.normalization
        # and the storage for the data likelihoods
        dataLLK = step.data

        # find out how many samples in the set
        samples = θ.rows
        # get the parameter sets
        psets = model.psets

        # get the offsets of the various parameter sets
        HsIdx = model.HsIdx
        HdIdx = model.HdIdx
        asIdx = model.asIdx
        adIdx = model.adIdx
        acIdx = model.acIdx

        # get the locations and times of the observations
        ticks = model.ticks
        # initialize a vector to hold the expected displacements
        u = altar.vector(shape=(3*model.observations))

        # for each sample in the sample set
        for sample in range(samples):
            # extract the parameters
            parameters = θ.getRow(sample)
            # get the locations of the chambers
            H_s = parameters[HsIdx]
            H_d = parameters[HdIdx]
            # get the sizes
            a_s = parameters[asIdx]
            a_d = parameters[adIdx]
            a_c = parameters[acIdx]

            # make a source using the sample parameters
            reverso = source(H_s=H_s, H_d=H_d,
                             a_s=a_s, a_d=a_d, a_c=a_c,
                             Qin=model.Qin,
                             G=model.G, v=model.v, mu=model.mu, drho=model.drho, g=model.g)

            # prime the displacement calculator
            predicted = reverso.displacements(locations=ticks)

            # compute the displacements
            for idx, ((t,x,y), (u_R,u_Z)) in enumerate(zip(ticks, predicted)):
                # find the polar angle of the vector to the observation location
                phi = math.atan2(y,x)
                # compute the E and N components
                u_E = u_R * math.sin(phi)
                u_N = u_R * math.cos(phi)
                # save
                u[3*idx + 0] = u_E
                u[3*idx + 1] = u_N
                u[3*idx + 2] = u_Z

            # subtract the observed displacements
            u -= displacements

            # compute the norm of the displacements
            nrm = norm.eval(v=u, sigma_inv=cd_inv)
            # normalize and store it as the data log likelihood
            dataLLK[sample] = normalization - nrm**2 /2

        # all done
        return self


# end of file
