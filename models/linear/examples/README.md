A benchmark multivariate Gaussian model 
======================================

The multivariate Gaussian pdf 

f({x_i}; {d_i}) = exp(-\sum_i(x_i -d_i)^2)/2\sigma^2  ; i= 1, N 

is similar to a Linear model with 

green = I ( identity matrix) 
cd = \sigma^2 I


We sample this model and expect, after annealing, 

mean(\theta_i) ~ d_i
sd(\theta_i) <= \sigma 

This can be checked by comparing the (mean, sd) report with the input data 
at `input/data.txt`. 



Usage
-----

run `python3 GenerateTestData.py` to generate an 8-parameter Gaussian model, which generates the input files for linear model in `input` directory. 

run `linear` to simulate the problem. Random samples as well as the prior/data likelihood/posterior at each step are saved in HDF5 format in results directory.
 
