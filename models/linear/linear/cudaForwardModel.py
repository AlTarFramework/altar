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
from altar.cuda import cublas,device    
 
def cudaForwardModel(theta, green, data_residuals=None, data_observations=None, batches=None):
    """
    Forward model: compute data prediction or data residuals from a set of theta 
    Args: 
        theta [in, cuarray] parameters with shape=(samples, parameters)
        green [in, cuarray] Green's function with shape = (observations, parameters)
        batches [in, integer, optional] number of samples needto be computed <=samples
        data_observations [in, cuarray, optional] data observations
        data_residuals[inout, cuarray, optional] data predictions or residuals shape=(observations, samples)
    Returns:
        data predictions or residuals if data_observations is provides 
    """
        
    # determine different sizes
    samples, parameters = theta.shape
    assert green.ndim == 2, "Green's function must be a 2D array"
    observations, parameters_g = green.shape
    assert parameters_g == parameters, "parameters in theta and Green's function don't match"
    
    # allocate a new data_residuals if not present
    if data_residuals is None:
        data_residuals = altar.cuda.cuarray(shape=(observations, samples))
    # if data_observations is available, copy it over
    if data_observations is not None:
        assert data_observations.shape == data_residuals.shape, "the shape of data_obs is not (obs, samples)" 
        data_residuals = data_observations.copy()
        beta = -1.0
    else:
        data_residuals.fill(0)
        beta = 0.0    
    
    if batches is None:
        batches = samples
        
    # grab cublas handle
    handle = altar.cuda.device.get_cublas_handle()
    # call cublas matrix multiplication 
    # cublas uses FORTRAN-major, for which each matrix in C-major should be viewed as its transpose
    # residuals viewed as (samples, observations)
    # G viewed as (parameters, observations) 
    # theta viewed as (parameters, samples) 
    # d_residuals =  transpose(theta) * Green  - d_obs  
    # (samples x parameters)x(parametersxobservations)->(samples x observations)
    cublas.dgemm(handle,
            1,  # transas
            0,  # transb
            batches, observations, parameters, #m,n,k
            1.0, # alpha
            theta.data.ptr, parameters, # A, lda
            green.data.ptr, parameters, #B, ldb
            beta, # beta
            data_residuals.data.ptr, samples) #C, ldc

    #all done
    return data_residuals
    
def gpuForwardModel(theta, green, data_residuals=None, data_observations=None, batches=None):
    """
    Same as cudaForwardModel, but uses CPU altar/gsl matrix as inputs/outputs
    """
    
    # copy data to gpu
    theta_gpu = altar.cuda.cuarray_from_matrix(matrix=theta)
    green_gpu = altar.cuda.cuarray_from_matrix(matrix=green)
    if data_observations is not None:
        data_obs_gpu = altar.cuda.cuarray_from_matrix(matrix=data_observations)
    else:
        data_obs_gpu = None
            
    # call cuda forward model computation routine
    data_res_gpu = cudaForwardModel(theta=theta_gpu, green=green_gpu, data_observations=data_obs_gpu, batches=batches)
    
    # copy results to cpu
    if data_residuals is None:
        data_residuals = altar.matrix(shape=data_res_gpu.shape)
    altar.cuda.copy_cuarray_to_matrix(data_res_gpu, data_residuals)
    
    # all done
    return data_residuals
