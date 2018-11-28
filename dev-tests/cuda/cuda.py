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

class cudaTest(altar.application):
    
    deviceID = altar.properties.int(default=0)
    size = altar.properties.int(default = 20)
    
    def test(self):
        device = altar.cuda.device.Device(self.deviceID)
        size = self.size
        
        offset = 10
        nsize = offset+size
        vec1o = altar.matrix(shape=(nsize,nsize)).fill(0)
        for i in range (size) : vec1o[i,i] = (i+1-offset)
        vec2 = altar.matrix(shape=(size,size)).fill(0)
        for i in range (size) : vec2[i,i] = 1.0/(i+1)
        prod = altar.matrix(shape=(size,size)).fill(0)
        
        
        vec1 = vec1o.view(start=(offset,offset), shape=(size,size))
        vec1.print()
        
        vec1_gpu = altar.cuda.cuarray_from_matrix(matrix=vec1)
        vec2_gpu = altar.cuda.cuarray_from_matrix(matrix=vec2)
        prod_gpu = altar.cuda.cuarray_from_matrix(matrix=prod)
         
        handle = altar.cuda.device.get_cublas_handle()
        #altar.cublas.ddot(handle, 
        #    size, 
        #    vec1.data.ptr, 1, 
        #    vec2.data.ptr, 1, 
        #    prod.data.ptr)
        altar.cuda.cublas.dgemm(handle,
                1,  # transa
                1,  # transb
                size, size, size, #m,n,k
                1, # alpha
                vec1_gpu.data.ptr, size,
                vec2_gpu.data.ptr, size,
                -1, 
                prod_gpu.data.ptr, size)
        print("The dot product is", prod_gpu)
        
        altar.cuda.copy_cuarray_to_matrix(cuarray=prod_gpu, matrix=prod)
        #prod.print()
        
        return

# bootstrap
if __name__ == "__main__":
    # create a test instance, name would be the pfg file name
    app=cudaTest(name='')
    # run the test
    status = app.test()
    # share
    raise SystemExit(status)
