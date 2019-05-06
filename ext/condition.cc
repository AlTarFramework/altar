// -*- C++ -*-
//
// (c) 2013-2019 parasim inc
// (c) 2010-2019 california institute of technology
// all rights reserved
//

#include <portinfo>
#include <Python.h>
#include <cmath>
#include <iostream>
#include <iomanip>

#include <gsl/gsl_sys.h>
#include <gsl/gsl_min.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_roots.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_matrix.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_statistics.h>
#include <gsl/gsl_blas.h>
#include <gsl/gsl_sort_vector.h>
#include <gsl/gsl_eigen.h>

#include <pyre/journal.h>
#include <pyre/gsl/capsules.h>

// local includes
#include "condition.h"
#include "capsules.h"

// uniform distribution
// uniform_sample
const char * const altar::extensions::matrix_condition__name__ = "matrix_condition";
const char * const altar::extensions::matrix_condition__doc__ =
    "condition a matrix to be positive definite";

PyObject *
altar::extensions::matrix_condition(PyObject *, PyObject * args) {
    // the arguments
    PyObject * matrixCapsule;
    double eval_ratio_min;
    // build my debugging channel
    pyre::journal::debug_t debug("altar.matrix_condition");

    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!d:matrix_condition",
                                  &PyCapsule_Type, &matrixCapsule,
                                  &eval_ratio_min);
    // if something went wrong
    if (!status) return 0;
    // bail out if the {matrix} capsule is not valid
    if (!PyCapsule_IsValid(matrixCapsule, gsl::matrix::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule");
        return 0;
    }

    // get the {sigma} matrix
    gsl_matrix * sigma =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(matrixCapsule, gsl::matrix::capsule_t));

    // get matrix size
    size_t m = sigma->size1;

    // solve the eigen value problem
    gsl_vector *eval = gsl_vector_alloc (m);
    gsl_matrix *evec = gsl_matrix_alloc (m, m);
    gsl_eigen_symmv_workspace * w = gsl_eigen_symmv_alloc (m);

    gsl_eigen_symmv (sigma, eval, evec, w);
    gsl_eigen_symmv_free (w);

    // sort the eigen values in ascending order (magnitude)
    gsl_eigen_symmv_sort (eval, evec,  GSL_EIGEN_SORT_ABS_ASC);

    // make a transpose of the eigen vector matrix
    gsl_matrix *evecT = gsl_matrix_alloc(m,m);
    gsl_matrix_transpose_memcpy(evecT, evec);

    // allocate a matrix for conditioned eigen values
    gsl_matrix *diagM = gsl_matrix_calloc(m,m);

    // set the minimum eigen value as the max * ratio
    double eval_min = eval_ratio_min*gsl_vector_get(eval,m-1);
    double eval_i;
    // copy the eigenvalues, set it to eval_min if smaller
    for (size_t i = 0; i < m; i++)
    {
        eval_i  = gsl_vector_get (eval, i);
        if (eval_i<eval_min) gsl_matrix_set(diagM, i, i, eval_min);
        else gsl_matrix_set(diagM, i, i, eval_i);
    }

    // reconstruct sigma from the conditioned eigen values
    gsl_matrix *tmp = gsl_matrix_alloc(m,m);
    gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, diagM, evecT, 0.0, tmp);
    gsl_blas_dgemm(CblasNoTrans, CblasNoTrans, 1.0, evec, tmp, 0.0, sigma);

    // make sigma symmetric
    gsl_matrix_transpose_memcpy(tmp, sigma);
    gsl_matrix_add(sigma,tmp);
    gsl_matrix_scale(sigma, 0.5);

    // free temporary data
    gsl_vector_free (eval);
    gsl_matrix_free (evec);
    gsl_matrix_free (evecT);
    gsl_matrix_free (diagM);
    gsl_matrix_free (tmp);

    // all done
    // return None
    Py_INCREF(Py_None);
    return Py_None;
}

// end of file
