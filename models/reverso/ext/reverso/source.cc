// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2020 parasim inc
// all rights reserved
//

// configuration
#include <portinfo>
// external
#include <Python.h>
#include <gsl/gsl_matrix.h>
#include <pyre/journal.h>
#include <pyre/gsl/capsules.h>

// the implementation
#include <altar/models/reverso/Source.h>
// my header
#include "source.h"
// the capsules
#include "capsules.h"

// type aliases
using source_t = altar::models::reverso::source_t;
// local names for external capsules
static const char * const vector_capst = gsl::vector::capsule_t;
static const char * const matrix_capst = gsl::matrix::capsule_t;
static const char * const matrix_view_capst = gsl::matrix::view_t;

// helpers
static void freeSource(PyObject *);


// newSource
const char * const
altar::extensions::models::reverso::
newSource__name__ = "newSource";

const char * const
altar::extensions::models::reverso::
newSource__doc__ = "create a new source";

PyObject *
altar::extensions::models::reverso::
newSource(PyObject *, PyObject * args)
{
    // storage
    double Qin;
    double G;
    double v;
    double mu;
    double drho;
    double g;
    // extract the material parameters
    int status = PyArg_ParseTuple(args,
                                  "dddddd:newSource",
                                  &Qin,
                                  &G, &v, &mu, &drho, &g);
    // if something went wrong
    if (!status) {
        // complain
        return 0;
    }

    // make a new source
    source_t * source = new source_t(Qin, G, v, mu, drho, g);
    // wrap it in a capsule and return it
    return PyCapsule_New(source, source_capst, freeSource);
}


// data
const char * const
altar::extensions::models::reverso::
data__name__ = "data";

const char * const
altar::extensions::models::reverso::
data__doc__ = "attach the observed displacements";

PyObject *
altar::extensions::models::reverso::
data(PyObject *, PyObject * args)
{
    // storage
    PyObject * pySource;
    PyObject * pyData;

    // unpack the arguments
    int status = PyArg_ParseTuple(args,
                                  "O!O!:data",
                                  &PyCapsule_Type, &pySource,
                                  &PyCapsule_Type, &pyData);
    // if something went wrong
    if (!status) {
        // complain
        return 0;
    }

    // if the source capsule is not valid
    if (!PyCapsule_IsValid(pySource, source_capst)) {
        // set up an error message
        PyErr_SetString(PyExc_TypeError, "invalid source capsule");
        // and complain
        return 0;
    }
    // if the LOS matrix capsule is not valid
    if (!PyCapsule_IsValid(pyData, vector_capst)) {
        // set up an error message
        PyErr_SetString(PyExc_TypeError, "invalid data vector capsule");
        // and complain
        return 0;
    }

    // unpack the source capsule
    source_t * source = static_cast<source_t *>(PyCapsule_GetPointer(pySource, source_capst));
    // unpack the data capsule
    gsl_vector * data = static_cast<gsl_vector *>(PyCapsule_GetPointer(pyData, vector_capst));

    // make channel
    pyre::journal::debug_t channel("reverso.source");
    // sign on
    channel
        << pyre::journal::at(__HERE__)
        << "attaching the data vector at " << data
        << pyre::journal::endl;

    // attach the locations to the source
    source->data(data);

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}


// locations
const char * const
altar::extensions::models::reverso::
locations__name__ = "locations";

const char * const
altar::extensions::models::reverso::
locations__doc__ = "attach the coordinates of the observation points to a source";

PyObject *
altar::extensions::models::reverso::
locations(PyObject *, PyObject * args)
{
    // storage
    PyObject * pySource;
    PyObject * pyLocations;

    // unpack the arguments
    int status = PyArg_ParseTuple(args,
                                  "O!O!:locations",
                                  &PyCapsule_Type, &pySource,
                                  &PyList_Type, &pyLocations);
    // if something went wrong
    if (!status) {
        // complain
        return 0;
    }

    // if the source capsule is not valid
    if (!PyCapsule_IsValid(pySource, source_capst)) {
        // set up an error message
        PyErr_SetString(PyExc_TypeError, "invalid source capsule");
        // and complain
        return 0;
    }

    // unpack the capsule
    source_t * source = static_cast<source_t *>(PyCapsule_GetPointer(pySource, source_capst));

    // make channel
    pyre::journal::debug_t channel("reverso.source");

    // find out how many locations there are
    std::size_t len = PyList_Size(pyLocations);
    // allocate a GSL matrix to hold the locations
    gsl_matrix * locations = gsl_matrix_alloc(len, 3);
    // go through each list entry
    for (std::size_t loc = 0; loc < len; ++loc) {
        // each list item is a tuple of the x, y coordinates of the observation point
        PyObject * vec = PyList_GET_ITEM(pyLocations, loc);
        // go through the coordinates
        for (std::size_t axis = 0; axis < 3; ++axis) {
            // grab the value
            double value = PyFloat_AsDouble(PyTuple_GET_ITEM(vec, axis));
            // if something went wrong
            if (PyErr_Occurred()) {
                // free the matrix
                gsl_matrix_free(locations);
                // and complain
                return 0;
            }
            // and assign them to the locations matrix
            gsl_matrix_set(locations, loc, axis, value);
        }
    }

    // sign on
    channel
        << pyre::journal::at(__HERE__)
        << "attaching observation locations matrix at " << locations
        << pyre::journal::endl;
    // attach the locations to the source
    source->locations(locations);

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}


// layout
const char * const
altar::extensions::models::reverso::
layout__name__ = "layout";

const char * const
altar::extensions::models::reverso::
layout__doc__ = "the parameter set layout";

PyObject *
altar::extensions::models::reverso::
layout(PyObject *, PyObject * args)
{
    // storage
    PyObject * pySource;
    std::size_t HsIdx, HdIdx, asIdx, adIdx, acIdx;

    // unpack the arguments
    int status = PyArg_ParseTuple(args,
                                  "O!kkkkk:layout",
                                  &PyCapsule_Type, &pySource,
                                  &HsIdx, &HdIdx, &asIdx, &adIdx, &acIdx);
    // if something went wrong
    if (!status) {
        // complain
        return 0;
    }

    // if the source capsule is not valid
    if (!PyCapsule_IsValid(pySource, source_capst)) {
        // set up an error message
        PyErr_SetString(PyExc_TypeError, "invalid source capsule");
        // and complain
        return 0;
    }

    // unpack the capsule
    source_t * source = static_cast<source_t *>(PyCapsule_GetPointer(pySource, source_capst));

    // make channel
    pyre::journal::debug_t channel("reverso.source");
    // sign on
    channel
        << pyre::journal::at(__HERE__)
        << "informing the source about the parameter set layout"
        << pyre::journal::endl;

    // attach the map
    source->layout(HsIdx, HdIdx, asIdx, adIdx, acIdx);

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}


// displacements
const char * const
altar::extensions::models::reverso::
displacements__name__ = "displacements";

const char * const
altar::extensions::models::reverso::
displacements__doc__ = "compute the predicted displacements";

PyObject *
altar::extensions::models::reverso::
displacements(PyObject *, PyObject * args)
{
    // storage
    PyObject * pySource;        // the source
    PyObject * pySamples;       // the matrix view with my parameters
    PyObject * pyDisplacements; // the matrix that will hold the predicted displacements

    // unpack the arguments
    int status = PyArg_ParseTuple(args,
                                  "O!O!O!:displacements",
                                  &PyCapsule_Type, &pySource,
                                  &PyCapsule_Type, &pySamples,
                                  &PyCapsule_Type, &pyDisplacements);
    // if something went wrong
    if (!status) {
        // complain
        return 0;
    }

    // if the source capsule is not valid
    if (!PyCapsule_IsValid(pySource, source_capst)) {
        // set up an error message
        PyErr_SetString(PyExc_TypeError, "invalid source capsule");
        // and complain
        return 0;
    }
    // if the matrix with the samples is not valid
    if (!PyCapsule_IsValid(pySamples, matrix_view_capst)) {
        // set up an error message
        PyErr_SetString(PyExc_TypeError, "invalid samples matrix capsule");
        // and complain
        return 0;
    }
    // if the matrix that will hold the predicted displacements is not valid
    if (!PyCapsule_IsValid(pyDisplacements, matrix_capst)) {
        // set up an error message
        PyErr_SetString(PyExc_TypeError, "invalid displacements matrix capsule");
        // and complain
        return 0;
    }

    // unpack the source capsule
    source_t * source =
        static_cast<source_t *>(PyCapsule_GetPointer(pySource, source_capst));
    // the capsule with the samples
    gsl_matrix_view * samples =
        static_cast<gsl_matrix_view *>(PyCapsule_GetPointer(pySamples, matrix_view_capst));
    // and the matrix with the predictions
    gsl_matrix * displ =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(pyDisplacements, matrix_capst));

    // make a channel
    pyre::journal::debug_t channel("reverso.source");
    // show me
    channel
        << pyre::journal::at(__HERE__) << pyre::journal::newline
        << "source: " << source << pyre::journal::newline
        << "samples: " << samples << pyre::journal::newline
        << "displacements: " << displ
        << pyre::journal::endl;

    // compute the predictions based on the sample parameters
    source->displacements(samples, displ);

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}


// residuals
const char * const
altar::extensions::models::reverso::
residuals__name__ = "residuals";

const char * const
altar::extensions::models::reverso::
residuals__doc__ = "compute the residuals";

PyObject *
altar::extensions::models::reverso::
residuals(PyObject *, PyObject * args)
{
    // storage
    PyObject * pySource;        // the source
    PyObject * pyDisplacements; // the matrix with the predicted displacements

    // unpack the arguments
    int status = PyArg_ParseTuple(args,
                                  "O!O!:residuals",
                                  &PyCapsule_Type, &pySource,
                                  &PyCapsule_Type, &pyDisplacements);
    // if something went wrong
    if (!status) {
        // complain
        return 0;
    }

    // if the source capsule is not valid
    if (!PyCapsule_IsValid(pySource, source_capst)) {
        // set up an error message
        PyErr_SetString(PyExc_TypeError, "invalid source capsule");
        // and complain
        return 0;
    }
    // if the matrix that will hold the predicted displacements is not valid
    if (!PyCapsule_IsValid(pyDisplacements, matrix_capst)) {
        // set up an error message
        PyErr_SetString(PyExc_TypeError, "invalid displacements matrix capsule");
        // and complain
        return 0;
    }

    // unpack the source capsule
    source_t * source =
        static_cast<source_t *>(PyCapsule_GetPointer(pySource, source_capst));
    // and the matrix with the predictions
    gsl_matrix * displ =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(pyDisplacements, matrix_capst));

    // make a channel
    pyre::journal::debug_t channel("reverso.source");
    // show me
    channel
        << pyre::journal::at(__HERE__) << pyre::journal::newline
        << "source: " << source << pyre::journal::newline
        << "displacements: " << displ
        << pyre::journal::endl;

    // compute the predictions based on the sample parameters
    source->residuals(displ);

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}


// helper definitions
void freeSource(PyObject * capsule) {
    const char * const source_capst = altar::extensions::models::reverso::source_capst;
    // bail out if the capsule is not valid
    if (!PyCapsule_IsValid(capsule, source_capst)) return;
    // get the matrix
    source_t * source =
        reinterpret_cast<source_t *>(PyCapsule_GetPointer(capsule, source_capst));
    // deallocate
    delete source;
    // all done
    return;
}

// end of file
