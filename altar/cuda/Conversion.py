# -*- python -*-
# -*- coding: utf-8 -*-
#
# Lijun Zhu (ljzhu@caltech.edu)
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# conversion between cupy.ndarray and altar/gsl matrix/vector

#support 
import altar
import cupy
import ctypes

def cuarray_from_matrix(matrix):
        
    """ 
    Create a cuArray instance from altar/gsl matrix
    Args: take either shape matrix or vector as inputs
    """
    # get the shape    
    shape = matrix.shape
    # initialize a cupy.ndarray
    array = cupy.ndarray(shape=shape)
    # copy the data 
    copy_cuarray_from_matrix(array, matrix)
    # all done    
    return array 
    
    
def copy_cuarray_from_matrix(cuarray, matrix):
    """
    copy from an altar/gsl matrix of the same shape
    cuarray has already been allocated
    """
    # get the memory address of the gsl matrix data
    matrix_address = ctypes.c_void_p(matrix.dataptr())
    # get the copy size in bytes
    nbytes = cuarray.nbytes 
    # call copy 
    cuarray.data.copy_from_host(matrix_address, nbytes)
            
    # all done
    return 
 
def copy_cuarray_to_matrix(cuarray, matrix):
    """
    copy from an altar/gsl matrix of the same shape
    cuarray has already been allocated
    """
    # get the memory address of the gsl matrix data
    matrix_address = ctypes.c_void_p(matrix.dataptr())
    # compute the copy size in bytes
    nbytes = cuarray.nbytes # assume double 
    # call copy 
    cuarray.data.copy_to_host(matrix_address, nbytes)
        
    # all done
    return 
        
# end of file
