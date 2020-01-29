# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2020 parasim inc
# (c) 2010-2020 california institute of technology
# all rights reserved
#


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
        xIdx = model.xIdx
        yIdx = model.yIdx
        dIdx = model.dIdx
        openingIdx = model.openingIdx
        aXIdx = model.aXIdx
        aYIdx = model.aYIdx
        aZIdx = model.aZIdx
        omegaXIdx = model.omegaXIdx
        omegaYIdx = model.omegaYIdx
        omegaZIdx = model.omegaZIdx
        offsetIdx = model.offsetIdx

        # get the observations
        los = model.los
        oid = model.oid
        locations = model.points
        observations = model.observations

        # for each sample in the sample set
        for sample in range(samples):
            # extract the parameters
            parameters = θ.getRow(sample)
            # get the location of the source
            x = parameters[xIdx]
            y = parameters[yIdx]
            # its depth
            d = parameters[dIdx]
            # and its opening
            opening = parameters[openingIdx]

            # get the semi-axis information
            aX = parameters[aXIdx]
            aY = parameters[aYIdx]
            aZ = parameters[aZIdx]
            omegaX = parameters[omegaXIdx]
            omegaY = parameters[omegaYIdx]
            omegaZ = parameters[omegaZIdx]

            # make a source using the sample parameters
            cdm = source(x=x, y=y, d=d, opening=opening,
                         ax=aX, ay=aY, az=aZ, omegaX=omegaX, omegaY=omegaY, omegaZ=omegaZ,
                         v=model.nu)
            # compute the expected displacement
            u = cdm.displacements(locations=locations, los=los)

            # subtract the observed displacements
            u -= displacements
            # adjust using the offset
            for obs in range(observations):
                # appropriate for the corresponding dataset
                u[obs] -= parameters[offsetIdx + oid[obs]]

            # compute the norm of the displacements
            nrm = norm.eval(v=u, sigma_inv=cd_inv)
            # normalize and store it as the data log likelihood
            dataLLK[sample] = normalization - nrm**2 /2

        # all done
        return self


# end of file
