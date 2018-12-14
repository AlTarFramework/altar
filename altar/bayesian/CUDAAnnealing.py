# -*- python -*-
# -*- coding: utf-8 -*-
#
# Lijun Zhu
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

#support
import altar

# superclass
from .AnnealingMethod import AnnealingMethod
from .SequentialAnnealing import SequentialAnnealing

# declaration
class CUDAAnnealing(SequentialAnnealing):
    """
    Implementation that takes advantage of CUDA on gpus to accelerate the computation
    """
    
    # interface
    def initialize(self, application):
        """
        Initialize me and my parts given an {application} context
        """
        
        # initialize super class (mpi)
        super().initialize(application=application)
        # determine the device ID
        rank = self.rank
        gpus = application.job.gpus
        self.deviceID = rank % gpus
        # initialize  
        self.device = altar.cuda.device.Device(self.deviceID) 
        self.device.use()

        # chain ups
        return 

    device=None
    deviceID=None


# end of file
