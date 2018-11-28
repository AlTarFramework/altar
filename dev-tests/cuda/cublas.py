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
    m = altar.properties.int(default = 6)
    n = altar.properties.int(default = 10)
    k = altar.properties.int(default = 8)
    
    def test(self):
        
        m = self.m
        n = self.n
        k = self.k
        
        device = altar.cuda.device.Device(self.deviceID)
        
        vec1 = altar.matrix(shape=(m,k)).fill(0)
        size = min(m, k)
        for i in range (size-1) : vec1[i,i+1] = (i+1)
        
        vec2 = altar.matrix(shape=(k,n)).fill(0)
        size = min(k,n)
        for i in range (size) : vec2[i,i] = 1.0/(i+1)
        
        prod = altar.matrix(shape=(m,n)).fill(0)        
        prod = altar.blas.dgemm(vec1.opNoTrans, vec1.opNoTrans, 1.0, vec1, vec2, 0.0, prod)
        
        print("cpu result")
        prod.print()
                
        vec1_gpu = altar.cuda.cuarray_from_matrix(matrix=vec1)
        vec2_gpu = altar.cuda.cuarray_from_matrix(matrix=vec2)
        prod_gpu = altar.cuda.cuarray_from_matrix(matrix=prod)
         
        handle = device.cublas_handle

        #print(vec1_gpu, vec2_gpu, prod_gpu, vec1_gpu.data.ptr)
        
        # C-Major to FORTRAN
        # vec1  (k, m) leading k   
        # vec2  (n, k) leading n
        # prod (n, m) leading n
        
        altar.cuda.cublas.dgemm(handle,
                0,  # transa
                0,  # transb
                n, m, k, #m,n,k
                1.0, # alpha
                vec2_gpu.data.ptr, n,
                vec1_gpu.data.ptr, k,
                0.0, 
                prod_gpu.data.ptr,n)
        print("The product is", prod_gpu)
        
        #altar.cuda.copy_cuarray_to_matrix(cuarray=prod_gpu, matrix=prod)
        #print("gpu result", prod)
        prod.print()
        
        
        
        
        return

# bootstrap
if __name__ == "__main__":
    # create a test instance, name would be the pfg file name
    app=cudaTest(name='')
    # run the test
    status = app.test()
    # share
    raise SystemExit(status)
