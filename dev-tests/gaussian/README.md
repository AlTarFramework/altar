A benchmark N-parameter Gaussian model 
======================================

The N-parameter Gaussian pdf 

f({x_i}; {d_i}) = exp(-\sum_i(x_i -d_i)^2)/2\sigma^2  ; i= 1, N 

is similar to a Linear model with 

green = I ( identity matrix) 
cd = \sigma^2 I


We sample this model and expect, after annealing, 

mean(\theta_i) = d_i
sd(\theta_i) <= \sigma 


Usage
-----

run `GenerateTestData.py` to generate an 8-parameter Gaussian model, with input files in `input` directory. 

run `linear` (CPU) or `culinear` (GPU) to simulate the problem. 
 
