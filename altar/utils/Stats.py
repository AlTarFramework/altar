# -*- python -*-
# -*- coding: utf-8 -*-
#
# Lijun Zhu (ljzhu@caltech.edu)
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


#support
import altar

def mean(theta):
    """
    Calculate the mean of a vector/matrix
    Args:
        theta as a vector or matrix
    Returns:
        the mean value, a value/vector if theta is a vector/matrix
    """
    # if vector, return mean value
    if isinstance(theta, altar.vector):
        result = theta.mean()
    # if matrix=samples, parameters, return mean values of each parameter
    elif isinstance(theta, altar.matrix):
        samples, parameters = theta.shape
        result = altar.vector(shape=parameters)
        for i in range(parameters):
            result[i] = theta.getColumn(i).mean()
    else:
        result = 0
    # all done
    return result

def sdev(theta, mean=None):
    """
    Calculate the standard deviation of a vector/matrix
    Args:
        theta as a vector or matrix
        mean (optional): a given or precalculated mean
    Returns:
        sdev the mean value, a value/vector if theta is a vector/matrix
    """
    # if vector, return mean value
    if isinstance(theta, altar.vector):
        result = theta.sdev(mean=mean)
    # if matrix=samples, parameters, return sdev values of each parameter
    elif isinstance(theta, altar.matrix):
        samples, parameters = theta.shape
        result = altar.vector(shape=parameters)
        for i in range(parameters):
            result[i] = theta.getColumn(i).sdev(mean=mean)
    else:
        result = 0
    # all done
    return result

def mean_sd(theta):
    """
    Calculate both the mean and standard deviation of a vector/matrix
    Args:
        theta vector or matrix
    Returns:
        mean: the mean value
        sd: the standard deviation
    """
    # if vector, return mean value
    if isinstance(theta, altar.vector):
        mean = theta.mean()
        sd = theta.sdev(mean=mean)
    # if matrix=samples, parameters, return sdev values of each parameter
    elif isinstance(theta, altar.matrix):
        samples, parameters = theta.shape
        mean = altar.vector(shape=parameters)
        sd = altar.vector(shape=parameters)
        for i in range(parameters):
            pset = theta.getColumn(i)
            mean[i] = pset.mean()
            sd[i] = pset.sdev(mean=mean[i])
    else:
        mean, sd = 0, 0
    # all done
    return mean, sd

# end of file
