Benchmark problem: N-parameter multivariate Gaussian model
==========================================================

The pdf for N-parameter multivariate Gaussian model is

f({x_i}; {d_i}) = exp(-\sum_i(x_i -d_i)^2)/2\sigma^2  ; i= 1, N.

This is equivalent to a Linear model with

green = I ( identity matrix)
cd = \sigma^2 I

We offer two examples here: N=8, and N=100, in 8p and 100p directories, respectively.

Altar should produce final samples with

mean(\theta_i) = d_i, (check input/data.txt)
sd(\theta_i) <= \sigma. (sigma=0.01 in these examples)

Usage:
- run `linear` from the 8p or 100p directory,
- `cat input/data.txt` to check whether they are consistent with the final step Theta mean,
- check whether the final step Theta sdev are <= 0.01.