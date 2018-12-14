# -*- python -*-
# -*- coding: utf-8 -*-
#
# Lijun Zhu <ljzhu@caltech.edu>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# the package
import altar
# my protocol
from .Sampler import Sampler as sampler
# my super class
from .Metropolis import Metropolis

# declaration
class cudaMetropolis(Metropolis, family="altar.samplers.cudaMetropolis"):
    """
    The cuda Metropolis algorithm as a sampler of the posterior distribution
    """

    # protocol obligations
    @altar.export
    def initialize(self, application):
        """
        call cpu super class for initialization
        """
        super().initialize(application=application)
        print("cuda Metropolis initialized")
        return self


    # implementation details
    def prepareSamplingPDF(self, annealer, step):
        """
        Re-scale and decompose the parameter covariance matrix, in preparation for the
        Metropolis update
        """
        #call cpu super class method
        super().prepareSamplingPDF(annealer=annealer, step=step)
        #copy cpu sigma to gpu
        #self.sigma_chol.view(start=(0,0), shape=(3,3)).print()
        self.d_sigma_chol = altar.cuda.cuarray_from_matrix(self.sigma_chol)

        # all done
        return self

    def displace(self, sample):
        """
        Construct a set of displacement vectors for the random walk from a distribution with zero
        mean and my covariance
        """
        # get my decomposed covariance
        d_sigma_chol = self.d_sigma_chol

        # randomize delta_theta with N(0, 1) sampels
        samples, parameters = sample.shape
        d_delta_theta = altar.cuda.random.randn(samples, parameters)

        # copy the samples to gpu
        d_theta_proposal = altar.cuda.cuarray_from_matrix(sample)

        # multi the displacement by the decomposed covariance matrix
        # theta_proposal =  sigma_col * delta_theta  + theta
        # grab cublas handle
        handle = altar.cuda.device.get_cublas_handle()
        # call cublas matrix multiplication
        # cublas uses FORTRAN-major, for which each matrix in C-major should be viewed as its transpose
        # theta, theta_proposal, delta_theta viewed as (parameters, samples)
        # sigma_chol as (parameters, parameters) the same 
        # sigma_col * delta_theta: (parameters, parameters)*(parameters, samples) ->(parameters, samples)
        altar.cuda.cublas.dsymm(handle,
            0,  # side left
            0,  # fill low
            parameters, samples, #m,n
            1.0, # alpha
            d_sigma_chol.data.ptr, parameters, # A, lda
            d_delta_theta.data.ptr, parameters, #B, ldb
            1.0, # beta
            d_theta_proposal.data.ptr, parameters) #C, ldc

        # allocate the transpose
        δ = altar.matrix(shape=sample.shape)
        # copy the proposal from cuda
        altar.cuda.copy_cuarray_to_matrix(d_theta_proposal, δ)

        # and return it
        return δ


    # gpu variables
    d_sigma_chol=None
    
# end of file
