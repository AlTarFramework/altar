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
from altar.models import seismic

class MomentTest(altar.shells.application):
    
    def test(self):
        # get class definition
        momentD = seismic.moment()
        # create an instance, name would be its identifier in pfg file 
        moment = momentD(name='moment') 
    
        #rng = altar.simulations.GSLRNG.GSLRNG()
        rng = self.rng    
    
        samples = 5
        parameters = 18
    
        theta = altar.matrix(shape=(samples, parameters)) # create a 
        theta.zero() # fill in zero
    
        probability = altar.vector(shape=samples).zero() 
        
        moment.initialize(rng)
        moment.initializeSample(theta)

        moment.computePrior(theta, probability)

        print("The generated samples:")
        theta.print()
        print("The prior probability:")
        probability.print()
        return
    
        
# bootstrap
if __name__ == "__main__":
    # create a test instance, name would be the pfg file name
    app=MomentTest(name='moment')
    # run the test
    status = app.test()
    # share
    raise SystemExit(status)
