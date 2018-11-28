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

class ListTest(altar.models.bayesian, family="altar.models.listtest"):
    
    arrays = altar.properties.list()
    numK = altar.properties.int(default=2)
    
    def test(self):
        
        array = altar.matrix(shape=(2,2))
        
        arrays = self.arrays
        
        print(arrays)
        print(self.numK)
        
        for i in range(self.numK) :
            array.fill(i)
            arrays.append(array)
        
        array1 = arrays[1]    
        print(array1[1,1])
        
        return self
        
# bootstrap
if __name__ == "__main__":
    # build an instance of the default app
    app = ListTest(name="ListTest")
    # invoke the main entry point
    status = app.test()
    # share
    raise SystemExit(status)
        
