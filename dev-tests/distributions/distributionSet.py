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

class DistributionSetTest(altar.shells.application):
    
    parameters = altar.properties.int(default=1)
    samples = altar.properties.int(default=1)
    
    def test(self):
        
        DistributionSetClass = altar.distributions.distributionset()
        dset = DistributionSetClass(name='dset')

        dset.initialize(self.rng)
        parameters = self.parameters
        print("total parameters", parameters)        
        
        samples = self.samples
        theta = altar.matrix(shape=(samples, parameters))
        theta.zero()
    
        dset.initializeSample(theta)
        theta.print()
        density = altar.vector(shape=samples).fill(0)
        dset.priorProbability(theta, density)
        density.print()
        return
    
        
# bootstrap
if __name__ == "__main__":
    #run the test
    app=DistributionSetTest(name='distributionSet')
    status = app.test()
    # share
    raise SystemExit(status)
        
