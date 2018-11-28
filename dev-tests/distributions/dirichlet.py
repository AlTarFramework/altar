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

class DirichletTest(altar.shells.application):
    
    def test(self):
        # get class definition
        dirichletD = altar.distributions.dirichlet()
        # create an instance, name would be its identifier in pfg file 
        dirichlet = dirichletD(name='dirichlet') 
    
        #rng = altar.simulations.GSLRNG.GSLRNG()
        rng = self.rng    
    
        samples = 5
        parameters = 10
    
        theta = altar.matrix(shape=(samples, parameters)) # create a 
        theta.zero() # fill in zero
    
        dirichlet.initialize(rng)
        dirichlet.initializeSample(theta)
        theta.print()
        return
    
        
# bootstrap
if __name__ == "__main__":
    # create a test instance, name would be the pfg file name
    app=DirichletTest(name='dirichlet')
    # run the test
    status = app.test()
    # share
    raise SystemExit(status)
