// -*- C++ -*-
//
// Lijun Zhu (ljzhu@caltech.edu)
//
// (c) 2013-2018 parasim inc
// (c) 2010-2018 california institute of technology
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

#include <pyre/journal.h>
#include <pyre/gsl/capsules.h>

// local includes
#include "distributions.h"
#include "capsules.h"

// uniform distribution
// uniform_sample
const char * const altar::extensions::uniform::sample__name__ = "uniform_sample";
const char * const altar::extensions::uniform::sample__doc__ =
    "uniform rng for a matrix";

PyObject *
altar::extensions::uniform::sample(PyObject *, PyObject * args) {
    // the arguments
    double low, high;
    PyObject * thetaCapsule;
    PyObject * rngCapsule;

    // build my debugging channel
    pyre::journal::debug_t debug("altar.distributions.uniform");

    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "(dd)O!O!:uniform_sample",
                                  &low, &high, 
                                  &PyCapsule_Type, &thetaCapsule, 
                                  &PyCapsule_Type, &rngCapsule
                                  );
    // if something went wrong
    if (!status) return 0;
    // bail out if the {theta} capsule is not valid
    if (!PyCapsule_IsValid(thetaCapsule, gsl::matrix::view_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for theta");
        return 0;
    }
    // bail out if the {rng} capsule is not valid
    if (!PyCapsule_IsValid(rngCapsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }

    // get the rng
    gsl_rng * rng = static_cast<gsl_rng *>(PyCapsule_GetPointer(rngCapsule, gsl::rng::capsule_t));
    
    // get the {theta} matrix (view)
    gsl_matrix_view * theta_view =
        static_cast<gsl_matrix_view *>(PyCapsule_GetPointer(thetaCapsule, gsl::matrix::view_t));
    gsl_matrix * theta = &(theta_view->matrix);

    // get the size
    const size_t samples =theta->size1;
    const size_t parameters = theta->size2;
    // ... and the sample matrix

    // for each sample
    for (size_t sample=0; sample<samples; ++sample)
    {   
        // for each index in the corresponding range
        for (size_t idx=0; idx<parameters; ++idx)
        {   
            // generate a gaussian
            gsl_matrix_set(theta, sample, idx, gsl_ran_flat(rng, low, high));
        }
    }

    // all done
    // return None                                                                                                                             
    Py_INCREF(Py_None);
    return Py_None;

}

const char * const altar::extensions::uniform::logpdf__name__ = "uniform_logpdf";
const char * const altar::extensions::uniform::logpdf__doc__ =
    "uniform compute log pdf";

PyObject *
altar::extensions::uniform::logpdf(PyObject *, PyObject * args) {
    // the arguments
    double low, high;
    PyObject * thetaCapsule;
    PyObject * pdfCapsule;
    
    // build my debugging channel
    pyre::journal::debug_t debug("altar.distributions.uniform");

    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "(dd)O!O!:gaussian_logpdf",
                                  &low, &high, 
                                  &PyCapsule_Type, &thetaCapsule, 
                                  &PyCapsule_Type, &pdfCapsule
                                  );
    // if something went wrong    
    if (!status) return 0;
    // bail out if the {pdf} capsule is not valid
    if (!PyCapsule_IsValid(pdfCapsule, altar::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid pdf capsule");
        return 0;
    }
    // bail out if the {theta} capsule is not valid
    if (!PyCapsule_IsValid(thetaCapsule, gsl::matrix::view_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for theta");
        return 0;
    }
    
    // get the {theta} matrix (view)
    gsl_matrix_view * theta_view =
        static_cast<gsl_matrix_view *>(PyCapsule_GetPointer(thetaCapsule, gsl::matrix::view_t));
    gsl_matrix * theta = &(theta_view->matrix);

    // get the {pdf} vector
    gsl_vector * pdf =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(pdfCapsule, altar::vector::capsule_t));
        
    // get the problem sizes
    const size_t samples = theta->size1;
    const size_t parameters = theta->size2;
    // ... and the sample matrix
    const size_t offset=0;

    double logpdf = parameters*log(high-low);
    // for each sample
    for (size_t sample=0; sample<samples; ++sample)
    {
        // store in the prior vector
        gsl_vector_set(pdf, sample, logpdf);
    }

    // all done
    // return None                                                                                                                             
    Py_INCREF(Py_None);
    return Py_None;
}

const char * const altar::extensions::uniform::verify__name__ = "uniform_verify";
const char * const altar::extensions::uniform::verify__doc__ =
    "uniform verify range";

PyObject *
altar::extensions::uniform::verify(PyObject *, PyObject * args) {
    // the arguments
    double low, high;
    PyObject * thetaCapsule;
    PyObject * maskCapsule;
    
    // build my debugging channel
    pyre::journal::debug_t debug("altar.distributions.uniform");

    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "(dd)O!O!:gaussian_logpdf",
                                  &low, &high, 
                                  &PyCapsule_Type, &thetaCapsule, 
                                  &PyCapsule_Type, &maskCapsule
                                  );
    // if something went wrong    
    if (!status) return 0;
    // bail out if the {pdf} capsule is not valid
    if (!PyCapsule_IsValid(maskCapsule, altar::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid mask capsule");
        return 0;
    }
    // bail out if the {theta} capsule is not valid
    if (!PyCapsule_IsValid(thetaCapsule, gsl::matrix::view_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for theta");
        return 0;
    }
    
    // get the {theta} matrix (view)
    gsl_matrix_view * theta_view =
        static_cast<gsl_matrix_view *>(PyCapsule_GetPointer(thetaCapsule, gsl::matrix::view_t));
    gsl_matrix * theta = &(theta_view->matrix);

    // get the {pdf} vector
    gsl_vector * mask =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(maskCapsule, altar::vector::capsule_t));
        
    // get the problem sizes
    const size_t samples = theta->size1;
    const size_t parameters = theta->size2;
    // ... and the sample matrix
    const size_t offset=0;

    double value;
    // for each sample
    for (size_t sample=0; sample<samples; ++sample)
    {   
        // for each index in the corresponding range
        for (size_t idx=0; idx<parameters; ++idx)
        {   
            // get the theta value
            value = gsl_matrix_get(theta, sample, idx);
            // if out of support range, set the flag in mask and go to next sample
            if(value < low || value > high) 
            {
                gsl_vector_set(mask, sample, 1);
                break;
            }
        }
    }

    // all done
    // return None                                                                                                                             
    Py_INCREF(Py_None);
    return Py_None;
}

// gaussian_sample
const char * const altar::extensions::gaussian::sample__name__ = "gaussian_sample";
const char * const altar::extensions::gaussian::sample__doc__ =
    "gaussian rng for a matrix";

PyObject *
altar::extensions::gaussian::sample(PyObject *, PyObject * args) {
    // the arguments
    double mean, sigma;
    PyObject * thetaCapsule;
    PyObject * rngCapsule;

    // build my debugging channel
    pyre::journal::debug_t debug("altar.distributions.gaussian");

    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "ddO!O!:gaussian_sample",
                                  &mean, &sigma, 
                                  &PyCapsule_Type, &thetaCapsule, 
                                  &PyCapsule_Type, &rngCapsule
                                  );
    // if something went wrong
    if (!status) return 0;
    // bail out if the {theta} capsule is not valid
    if (!PyCapsule_IsValid(thetaCapsule, gsl::matrix::view_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for theta");
        return 0;
    }
    // bail out if the {rng} capsule is not valid
    if (!PyCapsule_IsValid(rngCapsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }

    // get the rng
    gsl_rng * rng = static_cast<gsl_rng *>(PyCapsule_GetPointer(rngCapsule, gsl::rng::capsule_t));
    
    // get the {theta} matrix (view)
    gsl_matrix_view * theta_view =
        static_cast<gsl_matrix_view *>(PyCapsule_GetPointer(thetaCapsule, gsl::matrix::view_t));
    gsl_matrix * theta = &(theta_view->matrix);

    // get the size
    const size_t samples =theta->size1;
    const size_t parameters = theta->size2;
    // ... and the sample matrix

    // for each sample
    for (size_t sample=0; sample<samples; ++sample)
    {   
        // for each index in the corresponding range
        for (size_t idx=0; idx<parameters; ++idx)
        {   
            // generate a gaussian
            gsl_matrix_set(theta, sample, idx, gsl_ran_gaussian(rng, sigma)+ mean);
        }
    }

    // all done
    // return None                                                                                                                             
    Py_INCREF(Py_None);
    return Py_None;

}

const char * const altar::extensions::gaussian::logpdf__name__ = "gaussian_logpdf";
const char * const altar::extensions::gaussian::logpdf__doc__ =
    "gaussian compute log pdf";

PyObject *
altar::extensions::gaussian::logpdf(PyObject *, PyObject * args) {
    // the arguments
    double mean, sigma;
    PyObject * thetaCapsule;
    PyObject * pdfCapsule;
    
    // build my debugging channel
    pyre::journal::debug_t debug("altar.distributions.gaussian");

    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "ddO!O!:gaussian_logpdf",
                                  &mean, &sigma, 
                                  &PyCapsule_Type, &thetaCapsule, 
                                  &PyCapsule_Type, &pdfCapsule
                                  );
    // if something went wrong    
    if (!status) return 0;
    // bail out if the {pdf} capsule is not valid
    if (!PyCapsule_IsValid(pdfCapsule, altar::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid pdf capsule");
        return 0;
    }
    // bail out if the {theta} capsule is not valid
    if (!PyCapsule_IsValid(thetaCapsule, gsl::matrix::view_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid matrix capsule for theta");
        return 0;
    }

    // get the {theta} matrix (view)
    gsl_matrix_view * theta_view =
        static_cast<gsl_matrix_view *>(PyCapsule_GetPointer(thetaCapsule, gsl::matrix::view_t));
    gsl_matrix * theta = &(theta_view->matrix);

    // get the {pdf} vector
    gsl_vector * pdf =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(pdfCapsule, altar::vector::capsule_t));

    // get the problem sizes
    const size_t samples = theta->size1;
    const size_t parameters = theta->size2;
    // ... and the sample matrix
    const size_t offset=0;

    double logpdf,value,density;

    // gaussian pdf = { 1 \over \sqrt{2 pi sigma^2} } \exp (-x^2 / 2 \sigma^2)
    // log pdf = -x^2/2\sigma^2 - 0.5*log(2\pi\sigma^2)
    double sigma_pref = -0.5/(sigma*sigma);
    double logpref = -0.5*log(2*M_PI*sigma*sigma);

    // for each sample
    for (size_t sample=0; sample<samples; ++sample)
    {
        // initialize the prior likelihood
        logpdf = 0;
        // and every parameter
        for (size_t idx=offset; idx<parameters+offset; ++idx)
        {
            value = gsl_matrix_get(theta, sample, idx)-mean;
            density = value*value*sigma_pref+logpref;
            logpdf += density;
        }
        // store in the prior vector
        gsl_vector_set(pdf, sample, logpdf);
    }

    // all done
    // return None                                                                                                                             
    Py_INCREF(Py_None);
    return Py_None;
}


// end of file
