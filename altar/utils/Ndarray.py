# -*- python -*-
# -*- coding: utf-8 -*-
#
# Lijun Zhu (ljzhu@caltech.edu)
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# create a numpy ndarray wrapper for altar/gsl matrix/vector

#support 
import altar
import numpy
import ctypes

def matrix_asnumpy(matrix):
        
    """ 
    Create a numpy ndarray wrapper for altar/gsl matrix (any changes to data are mutual)
    Args: 
        matrix altar.matrix
    Return:
        2d numpy ndarray  
    """
    # get the memory address of the matrix
    data_pointer = ctypes.cast(matrix.dataptr(), ctypes.POINTER(ctypes.c_double))
    return numpy.ctypeslib.as_array(data_pointer, shape=matrix.shape)  
    
def vector_asnumpy(vector):
        
    """ 
    Create a numpy ndarray wrapper for altar/gsl matrix (any changes to data are mutual)
    Args: take either shape matrix or vector as inputs
    """
    # get the memory address of the vector
    data_pointer = ctypes.cast(vector.dataptr(), ctypes.POINTER(ctypes.c_double))
    # create a numpy wrapper and return
    return numpy.ctypeslib.as_array(data_pointer, shape=(vector.shape,)) 
    
def ndarray_from_matrix(matrix):
    """
    Create a numpy array from matrix
    """
    # create a wrapper
    ndarray = matrix_asnumpy(matrix)
    # return a copy
    return ndarray.copy()

def ndarray_from_vector(vector):
    """
    Create a numpy array from vector
    """
    # create a wrapper
    ndarray = vector_asnumpy(vector)
    # return a copy
    return ndarray.copy()    
        
        
# end of file
