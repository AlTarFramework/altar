// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
//
// (c) 2013-2019 parasim inc
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
#include <altar/models/cudacdm/Source.h>
// my header
#include "source.h"
// the capsules
#include "capsules.h"

// type aliases
using source_t = altar::models::cudacdm::source_t;
// local names for external capsules
static const char * const vector_capst = gsl::vector::capsule_t;
static const char * const matrix_capst = gsl::matrix::capsule_t;
static const char * const matrix_view_capst = gsl::matrix::view_t;

// helpers
static void freeSource(PyObject *);


// newSource
const char * const
altar::extensions::models::cudacdm::
newSource__name__ = "newSource";

const char * const
altar::extensions::models::cudacdm::
newSource__doc__ = "create a new source";

PyObject *
altar::extensions::models::cudacdm::
newSource(PyObject *, PyObject * args)
{
    // storage
    double nu;
    std::size_t samples;
    std::size_t parameters;
    std::size_t observations;
    // we don't accept any arguments, so check that we didn't get any
    int status = PyArg_ParseTuple(args,
                                  "kkkd:newSource",
                                  &parameters, &samples, &observations, &nu);
    // if something went wrong
    if (!status) {
        // complain
        return 0;
    }

    // make a new source
    source_t * source = new source_t(parameters, samples, observations, nu);

    // wrap it in a capsule and return it
    return PyCapsule_New(source, source_capst, freeSource);
}


// data
const char * const
altar::extensions::models::cudacdm::
data__name__ = "data";

const char * const
altar::extensions::models::cudacdm::
data__doc__ = "attach the observed displacements";

PyObject *
altar::extensions::models::cudacdm::
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
    pyre::journal::debug_t channel("cudacdm.source");
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
altar::extensions::models::cudacdm::
locations__name__ = "locations";

const char * const
altar::extensions::models::cudacdm::
locations__doc__ = "attach the coordinates of the observation points to a source";

PyObject *
altar::extensions::models::cudacdm::
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
    pyre::journal::debug_t channel("cudacdm.source");

    // find out how many locations there are
    std::size_t len = PyList_Size(pyLocations);
    // allocate a GSL matrix to hold the locations
    gsl_matrix * locations = gsl_matrix_alloc(len, 2);
    // go through each list entry
    for (std::size_t loc = 0; loc < len; ++loc) {
        // each list item is a tuple of the x, y coordinates of the observation point
        PyObject * vec = PyList_GET_ITEM(pyLocations, loc);
        // go through the coordinates
        for (std::size_t axis = 0; axis < 2; ++axis) {
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


// los
const char * const
altar::extensions::models::cudacdm::
los__name__ = "los";

const char * const
altar::extensions::models::cudacdm::
los__doc__ = "attach the coordinates of the observation points to a source";

PyObject *
altar::extensions::models::cudacdm::
los(PyObject *, PyObject * args)
{
    // storage
    PyObject * pySource;
    PyObject * pyLOS;

    // unpack the arguments
    int status = PyArg_ParseTuple(args,
                                  "O!O!:los",
                                  &PyCapsule_Type, &pySource,
                                  &PyCapsule_Type, &pyLOS);
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
    if (!PyCapsule_IsValid(pyLOS, matrix_capst)) {
        // set up an error message
        PyErr_SetString(PyExc_TypeError, "invalid LOS matrix capsule");
        // and complain
        return 0;
    }

    // unpack the source capsule
    source_t * source = static_cast<source_t *>(PyCapsule_GetPointer(pySource, source_capst));
    // and the LOS matrix capsule
    gsl_matrix * los = static_cast<gsl_matrix *>(PyCapsule_GetPointer(pyLOS, matrix_capst));

    // make channel
    pyre::journal::debug_t channel("cudacdm.source");
    // sign on
    channel
        << pyre::journal::at(__HERE__)
        << "attaching LOS matrix at " << los
        << pyre::journal::endl;

    // make a copy of the LOS matrix so {source} can own
    gsl_matrix * clone = gsl_matrix_alloc(los->size1, los->size2);
    // transfer the data
    gsl_matrix_memcpy(clone, los);
    // attach the los to the source
    source->los(clone);

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}


// oid
const char * const
altar::extensions::models::cudacdm::
oid__name__ = "oid";

const char * const
altar::extensions::models::cudacdm::
oid__doc__ = "attach the map of observations to the data set";

PyObject *
altar::extensions::models::cudacdm::
oid(PyObject *, PyObject * args)
{
    // storage
    PyObject * pySource;
    PyObject * pyOID;

    // unpack the arguments
    int status = PyArg_ParseTuple(args,
                                  "O!O!:oid",
                                  &PyCapsule_Type, &pySource,
                                  &PyList_Type, &pyOID);
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
    pyre::journal::debug_t channel("cudacdm.source");

    // find out how many observations there are
    std::size_t len = PyList_Size(pyOID);
    // allocate a vector to hold the data set map
    source_t::oids_type oids(len);
    // go through each list entry
    for (std::size_t oid = 0; oid < len; ++oid) {
        // get the corresponding dataset
        std::size_t dataset = PyLong_AsLong(PyList_GET_ITEM(pyOID, oid));
        // if something went wrong
        if (PyErr_Occurred()) {
            // complain
            return 0;
        }
        // assign the oid to this data set
        oids[oid] = dataset;
    }

    // sign on
    channel
        << pyre::journal::at(__HERE__)
        << "mapping observations to data sets"
        << pyre::journal::endl;

    // attach the map
    source->oids(oids);

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}


// layout
const char * const
altar::extensions::models::cudacdm::
layout__name__ = "layout";

const char * const
altar::extensions::models::cudacdm::
layout__doc__ = "the parameter set layout";

PyObject *
altar::extensions::models::cudacdm::
layout(PyObject *, PyObject * args)
{
    // storage
    PyObject * pySource;
    std::size_t xIdx, dIdx, openingIdx, aXIdx, omegaXIdx, offsetIdx;

    // unpack the arguments
    int status = PyArg_ParseTuple(args,
                                  "O!kkkkkk:layout",
                                  &PyCapsule_Type, &pySource,
                                  &xIdx, &dIdx,
                                  &openingIdx, &aXIdx, &omegaXIdx,
                                  &offsetIdx);

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
    pyre::journal::debug_t channel("cudacdm.source");
    // sign on
    channel
        << pyre::journal::at(__HERE__)
        << "informing the source about the parameter set layout"
        << pyre::journal::endl;

    // attach the map
    source->layout(xIdx, dIdx, openingIdx, aXIdx, omegaXIdx, offsetIdx);

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}


// residuals
const char * const
altar::extensions::models::cudacdm::
residuals__name__ = "residuals";

const char * const
altar::extensions::models::cudacdm::
residuals__doc__ = "compute the residuals";

PyObject *
altar::extensions::models::cudacdm::
residuals(PyObject *, PyObject * args)
{
    // storage
    PyObject * pySource;        // the source
    PyObject * pySamples;       // the matrix view with my parameters
    PyObject * pyDisplacements; // the matrix with the predicted displacements

    // unpack the arguments
    int status = PyArg_ParseTuple(args,
                                  "O!O!O!:residuals",
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
    // the samples
    gsl_matrix_view * samples =
        static_cast<gsl_matrix_view *>(PyCapsule_GetPointer(pySamples, matrix_view_capst));
    // and the matrix with the predictions
    gsl_matrix * displ =
        static_cast<gsl_matrix *>(PyCapsule_GetPointer(pyDisplacements, matrix_capst));

    // make a channel
    pyre::journal::debug_t channel("cudacdm.source");
    // show me
    channel
        << pyre::journal::at(__HERE__) << pyre::journal::newline
        << "source: " << source << pyre::journal::newline
        << "samples: " << samples << pyre::journal::newline
        << "displacements: " << displ
        << pyre::journal::endl;

    // compute the predictions based on the sample parameters
    source->residuals(samples, displ);

    // all done
    Py_INCREF(Py_None);
    return Py_None;
}


// helper definitions
void freeSource(PyObject * capsule) {
    const char * const source_capst = altar::extensions::models::cudacdm::source_capst;
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
