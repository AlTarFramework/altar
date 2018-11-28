# -*- python -*-
# -*- coding: utf-8 -*-
#
# michael a.g. aïvázis <michael.aivazis@para-sim.com>
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# the package
import altar

class UniformTest(altar.shells.application):
    
    def test(self):
        # get class definition
        uniformD = altar.distributions.uniform()
        # create an instance, name would be its identifier in pfg file 
        uniform = uniformD(name='uniform') 
    
        #rng = altar.simulations.GSLRNG.GSLRNG()
        rng = self.rng    
    
        samples = 5
        parameters = 10
    
        theta = altar.matrix(shape=(samples, parameters)) # create a 
        theta.zero() # fill in zero
    
        uniform.initialize(rng)
        uniform.initializeSample(theta)
        theta.print()
        return
    
        
# bootstrap
if __name__ == "__main__":
    # create a test instance, name would be the pfg file name
    app=UniformTest(name='uniform')
    # run the test
    status = app.test()
    # share
    raise SystemExit(status)
