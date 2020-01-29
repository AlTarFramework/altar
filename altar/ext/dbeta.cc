// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2020 parasim inc
// (c) 2010-2020 california institute of technology
// all rights reserved
//


#include <portinfo>
#include <Python.h>
#include <cmath>
#include <iostream>
#include <iomanip>

#include <altar/bayesian/COV.h>

#include <gsl/gsl_sys.h>
#include <gsl/gsl_min.h>
#include <gsl/gsl_rng.h>
#include <gsl/gsl_roots.h>
#include <gsl/gsl_vector.h>
#include <gsl/gsl_statistics.h>

#include <pyre/journal.h>
#include <pyre/gsl/capsules.h>

// local includes
#include "dbeta.h"
#include "capsules.h"


// dbeta
const char * const altar::extensions::dbeta_brent__name__ = "dbeta_brent";
const char * const altar::extensions::dbeta_brent__doc__ =
    "compute the next increment to the annealing temperature using the Brent algorithm from GSL";

PyObject *
altar::extensions::dbeta_brent(PyObject *, PyObject * args) {
    // the arguments
    PyObject * covCapsule;
    PyObject * llkCapsule;
    double llkMedian;
    PyObject * wCapsule;

    // build my debugging channel
    pyre::journal::debug_t debug("altar.beta");

    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!dO!:dbeta_brent",
                                  &PyCapsule_Type, &covCapsule,
                                  &PyCapsule_Type, &llkCapsule,
                                  &llkMedian,
                                  &PyCapsule_Type, &wCapsule
                                  );
    // if something went wrong
    if (!status) return 0;
    // bail out if the {cov} capsule is not valid
    if (!PyCapsule_IsValid(covCapsule, altar::extensions::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule for cov");
        return 0;
    }
    // bail out if the {llk} capsule is not valid
    if (!PyCapsule_IsValid(llkCapsule, altar::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule for llk");
        return 0;
    }
    // bail out if the {w} capsule is not valid
    if (!PyCapsule_IsValid(wCapsule, altar::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule for w");
        return 0;
    }

    // get the {cov}
    altar::bayesian::COV * cov =
        static_cast<altar::bayesian::COV *>
        (PyCapsule_GetPointer(covCapsule, altar::extensions::capsule_t));
    // get the {w} vector
    gsl_vector * w =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(wCapsule, altar::vector::capsule_t));
    // get the {llk} vector
    gsl_vector * llk =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(llkCapsule, altar::vector::capsule_t));

    // update
    cov->dbeta_brent(llk, llkMedian, w);

    // build a tuple for the result
    PyObject * answer = PyTuple_New(2);
    PyTuple_SET_ITEM(answer, 0, PyFloat_FromDouble(cov->beta()));
    PyTuple_SET_ITEM(answer, 1, PyFloat_FromDouble(cov->cov()));
    // all done
    return answer;
}

const char * const altar::extensions::dbeta_grid__name__ = "dbeta_grid";
const char * const altar::extensions::dbeta_grid__doc__ =
    "compute the next increment to the annealing temperature using an iterative grid search";

PyObject *
altar::extensions::dbeta_grid(PyObject *, PyObject * args) {
    // the arguments
    PyObject * covCapsule;
    PyObject * llkCapsule;
    double llkMedian;
    PyObject * wCapsule;

    // build my debugging channel
    pyre::journal::debug_t debug("altar.beta");

    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args, "O!O!dO!:dbeta_grid",
                                  &PyCapsule_Type, &covCapsule,
                                  &PyCapsule_Type, &llkCapsule,
                                  &llkMedian,
                                  &PyCapsule_Type, &wCapsule
                                  );
    // if something went wrong
    if (!status) return 0;
    // bail out if the {cov} capsule is not valid
    if (!PyCapsule_IsValid(covCapsule, altar::extensions::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule for cov");
        return 0;
    }
    // bail out if the {llk} capsule is not valid
    if (!PyCapsule_IsValid(llkCapsule, altar::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule for llk");
        return 0;
    }
    // bail out if the {w} capsule is not valid
    if (!PyCapsule_IsValid(wCapsule, altar::vector::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid vector capsule for w");
        return 0;
    }

    // get the {cov}
    altar::bayesian::COV * cov =
        static_cast<altar::bayesian::COV *>
        (PyCapsule_GetPointer(covCapsule, altar::extensions::capsule_t));
    // get the {w} vector
    gsl_vector * w =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(wCapsule, altar::vector::capsule_t));
    // get the {llk} vector
    gsl_vector * llk =
        static_cast<gsl_vector *>(PyCapsule_GetPointer(llkCapsule, altar::vector::capsule_t));

    // update
    cov->dbeta_grid(llk, llkMedian, w);

    // build a tuple for the result
    PyObject * answer = PyTuple_New(2);
    PyTuple_SET_ITEM(answer, 0, PyFloat_FromDouble(cov->beta()));
    PyTuple_SET_ITEM(answer, 1, PyFloat_FromDouble(cov->cov()));
    // all done
    return answer;
}

// COV
const char * const altar::extensions::cov__name__ = "cov";
const char * const altar::extensions::cov__doc__ =
    "allocate a COV instance to manage the annealing schedule";

PyObject *
altar::extensions::cov(PyObject *, PyObject * args) {
    // the arguments
    PyObject * rngCapsule;
    size_t maxiter;
    double tolerance;
    double target;

    // unpack the argument tuple
    int status = PyArg_ParseTuple(
                                  args,
                                  "O!kdd:cov",
                                  &PyCapsule_Type, &rngCapsule,
                                  &maxiter, &tolerance, &target
                                  );
    // if something went wrong, bail
    if (!status) return 0;

    // bail out if the rng capsule is not valid
    if (!PyCapsule_IsValid(rngCapsule, gsl::rng::capsule_t)) {
        PyErr_SetString(PyExc_TypeError, "invalid rng capsule");
        return 0;
    }

    // get the rng
    gsl_rng * rng = static_cast<gsl_rng *>(PyCapsule_GetPointer(rngCapsule, gsl::rng::capsule_t));

    // build a COV
    auto scheduler =
        new altar::bayesian::COV(rng, tolerance, maxiter, target);

    // all done
    return PyCapsule_New(scheduler, capsule_t, free);
}


// destructors
void
altar::extensions::free(PyObject * capsule)
{
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, capsule_t)) return;
    // get the COV object
    auto cov =
        static_cast<altar::bayesian::COV *>(PyCapsule_GetPointer(capsule, capsule_t));
    // deallocate
    delete cov;
    // and return
    return;
}


// end of file
