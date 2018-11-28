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
import h5py
import os
import numpy

def save_step(step, path=None):
    """
    Save Coolinging Step to HDF5 file
    Args:
        step altar.bayesian.CoolingStep 
        path altar.primitives.path 
    Returns:
        None
    """
    
    # determine the output name as "{path}/step_{iteration}.h5" 
    str_iteration = str(step.iteration).zfill(3) 
    if path is not None:
        str_path = path.path if isinstance(path, altar.primitives.path) else path
        if not os.path.exists(str_path):
            os.mkdir(str_path)
    else:
        str_path = '.'
    suffix = '.h5'
    filename = os.path.join(str_path, "step_"+str_iteration+suffix)
    
    f=h5py.File(filename, 'w')
    f.create_dataset('beta', data=numpy.asarray(step.beta))
    f.create_dataset('covariance', data=altar.utils.matrix_asnumpy(step.sigma))
    f.create_dataset('theta', data=altar.utils.matrix_asnumpy(step.theta))
    f.create_dataset('prior', data=altar.utils.vector_asnumpy(step.prior))
    f.create_dataset('likelihood', data=altar.utils.vector_asnumpy(step.data))
    f.create_dataset('posterior', data=altar.utils.vector_asnumpy(step.posterior))
    f.close()
    
    # all done
    return
    
    
def load_step(step, path=None, iteration=None):
    """
    Load Cooling step data from HDF5 file
    """
    
    # to be done
    return
    

        
# end of file
