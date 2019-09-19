# -*- python -*-
# -*- coding: utf-8 -*-
#
# eric m. gurrola <eric.gurrola@jpl.nasa.gov>
#
# (c) 2018 california institute of technology
# all rights reserved
#
#

# the pure python implementation of the REVERSO source
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
        # radius of the shallow reservoir
        asIdx = model.asIdx
        # radius of the connecting tube
        acIdx = model.acIdx
        # radius of the deep reservoir
        adIdx = model.adIdx
        # depth of the shallow reservoir
        hsIdx = model.hsIdx
        # depth of the shallow reservoir
        hdIdx = model.hdIdx
        # the basal magma flow rate
        qIdx  = model.qIdx

        # get the observations
        los = model.los
        oid = model.oid
        locations = model.points
        observations = model.observations

        # for each sample in the sample set
        for sample in range(samples):
            # extract the parameters
            parameters = θ.getRow(sample)
            # get the radius and depth of the shallow reservoir
            as = parameters[asIdx]
            hs = parameters[hsIdx]
            # get the radius and depth of the deep reservoir
            ad = parameters[adIdx]
            hd = parameters[hdIdx]
            # get the radius of the hydraulic pipe connecting the two reservoirs
            ac = parameters[acIdx]
            # get the basal magma inflow rate
            q  = parameters[qIdx]

            # make a source using the sample parameters
            reverso = source(as=as, hs=hs, ad=ad, hd=hd,
                         ax=aX, ay=aY, az=aZ, omegaX=omegaX, omegaY=omegaY, omegaZ=omegaZ,
                         v=model.nu)
            # compute the expected displacement
            u = reverso.displacements(locations=locations, los=los)

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
