#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Lijun Zhu (ljzhu@gps.caltech.edu)
#
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# Script to generate a N-dim Gaussian model for benchmarking
# treated as a Linear model with green = I (identity matrix)

# get the package
import altar
import os
import numpy as np

# make a specialized app that uses this model by default
class GenerateTestData(altar.shells.application):
    """
    A class to generate test data of N-dim Gaussian model
    """
    size = altar.properties.int(default=8)
    size.doc = "the dim of the Gaussian model"

    def main(self):
        nObservations = self.size
        # reset seed to 0 to generate same samples over different machines
        np.random.seed(0)
        # observations (data) are randomly set to values between -0.5, 0.5
        data = np.reshape(np.random.rand(nObservations).astype('float64'), (nObservations, 1))-0.5
        Cd = np.zeros((nObservations, nObservations), dtype=np.float64)
        gf = np.zeros((nObservations, nObservations), dtype=np.float64)
        for i in range (nObservations):
            Cd[i][i] = 1.0e-4 # 
            if i > 0:
                Cd[i-1][i] = Cd[i][i-1] = 1.0e-6
            gf[i][i] = 1.0
        
        # save the data
        path = "input"
        if not os.path.exists(path):
            os.mkdir(path)    
        np.savetxt(os.path.join(path,'data.txt'), data)
        np.savetxt(os.path.join(path,'cd.txt'), Cd)
        np.savetxt(os.path.join(path,'green.txt'), gf)
        # all done
        return 

# bootstrap
if __name__ == "__main__":
    # build an instance of the default app
    app = GenerateTestData()
    # invoke the main entry point
    status = app.main()
    # share
    raise SystemExit(status)



# end of file
