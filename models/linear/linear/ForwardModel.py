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

def forwardModel(theta, green, data_residuals=None, data_observations=None, batches=None):
    """
    Forward Model 
    Args:
         theta
    
    Returns: data_residuals (observations x samples) 
             as residuals (if data_observations is provided), or data prediction (if not)     
    """
    # copy the observed data is available, residuals are returned
    if data_observations is not None:
        data_residuals = data_observations.clone()
        beta = -1.0
    # no observed data, 
    elif data_residuals is None:
        observations = green.shape[0]
        samples = theta.shape[0]
        data_residuals = altar.matrix(shape=(observations, samples))
        beta = 0.0 
    else:
        beta = 0.0
    
    # compute G * transpose(θ) - d
    # we must transpose θ because its shape is (samples x parameters)
    # while the shape of G is (observations x parameters)
    # data_residuals is (observations x samples) 
    data_residuals = altar.blas.dgemm(green.opNoTrans, theta.opTrans, 1.0, green, theta, beta, data_residuals)
    
    # all done
    return data_residuals
