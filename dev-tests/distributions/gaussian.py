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

class GaussianTest(altar.shells.application):
    
    def test(self):
        # get class definition
        gaussianD = altar.distributions.gaussian()
        # create an instance, name would be its identifier in pfg file 
        gaussian = gaussianD(name="gaussian") 
    
        rng = self.rng    
    
        samples = 20
        parameters = 1
    
        theta = altar.matrix(shape=(samples, 20)) # create a 
        theta.zero() # fill in zero
    
        gaussian.initialize(rng)
        gaussian.offset = 2
        print(gaussian.mean)
        prob = altar.vector(shape=samples).fill(0)
        gaussian.priorProbability(theta, prob)
        #gaussian.initializeSample(theta)
        theta.print()
        prob.print()
        return
    
        
# bootstrap
if __name__ == "__main__":
    # create a test instance, name would be the pfg file name
    app=GaussianTest(name='strikeslip')
    # run the test
    status = app.test()
    # share
    raise SystemExit(status)
