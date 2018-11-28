# -*- python -*-
# -*- coding: utf-8 -*-
#
# Lijun Zhu
#
# (c) 2013-2018 parasim inc
# (c) 2010-2018 california institute of technology
# all rights reserved
#


# the package
import altar

# publish the packages in cupy
try:
    from cupy import ndarray as cuarray
    WITH_CUDA = True
except ImportError:
    WITH_CUDA = False

if WITH_CUDA: 
    from cupy.cuda import (
        #
        device, cublas, curand,
        )

    from .Conversion import (
        cuarray_from_matrix,
        copy_cuarray_from_matrix,
        copy_cuarray_to_matrix,
        )

# end of file
