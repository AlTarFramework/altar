# -*- python -*-
# -*- coding: utf-8 -*-
#
# Lijun Zhu
# 
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#

# test altar cuda model (imported cupy)

# the package
import altar

class CudaTest(altar.shells.application):
    
    deviceID = altar.properties.int(default=0)
    size = altar.properties.int(default = 64)
    
    def test(self):
        device = altar.cuda.device.Device(self.deviceID)
        size = self.size
        vec1 = altar.cuarray(shape=size)
        for i in range (size) : vec1[i] = i
        vec2 = altar.cuarray(shape=self.size)
        vec2.fill(10)
        prod = altar.cuarray(shape=1) 
        status = altar.cublas.ddot(device.cublas_handle, size, vec1.data.ptr, 1, vec2.data.ptr, 1, prod.data.ptr)
        print("The dot product is", prod)
        print("status", status)    
        
        return

# bootstrap
if __name__ == "__main__":
    # create a test instance, name would be the pfg file name
    app=CudaTest(name='')
    # run the test
    status = app.test()
    # share
    raise SystemExit(status)
