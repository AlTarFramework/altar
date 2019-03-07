// -*- C++ -*-
//
// michael a.g. aïvázis <michael.aivazis@para-sim.com>
// (c) 2013-2019 parasim inc
// all rights reserved
//

// code guard
#if !defined(altar_models_cudamogi_Source_h)
#define altar_models_cudamogi_Source_h

// external
#include <vector>

// forward declarations
namespace altar {
    namespace models {
        namespace cudamogi {
            // forwards declarations
            class Source;

            // type aliases
            using source_t = Source;
        }
    }
}


// the cudamogi source
class altar::models::cudamogi::Source {
    // types
public:
    using size_type = std::size_t;
    using data_type = double;
    using oids_type = std::vector<std::size_t>;

    // meta-methods
public:
    virtual ~Source();
    Source(size_type parameters, size_type samples, size_type observations, double nu);

    // interface
public:
    // information about the overall simulation
    void data(gsl_vector * data);
    void locations(gsl_matrix * locations);
    void los(gsl_matrix * los);
    void oids(const oids_type & oids);
    inline void layout(size_type xIdx, size_type dIdx, size_type sIdx, size_type offsetIdx);

    // compute the residuals
    void residuals(gsl_matrix_view * theta, gsl_matrix * residuals) const;

    // implementation details: methods
private:
    void _theta(gsl_matrix_view * theta) const;
    void _displacements() const;
    void _residuals() const;
    void _harvest(gsl_matrix * residuals) const;

    // implementation details: data
private:
    size_type _nSamples;        // the number of samples
    size_type _nParameters;     // the number of parameters
    size_type _nObservations;   // the number of parameters
    double _nu;                 // the Poisson ratio

    data_type * _data;          //
    data_type * _locations;     //
    data_type * _los;           //
    size_type * _oids;          //

    // the layout of the various parameters within a sample
    size_type _xIdx;
    size_type _yIdx;
    size_type _dIdx;
    size_type _sIdx;
    size_type _offsetIdx;

    data_type * _samples;       // buffer to hold the device copy of the samples
    data_type * _predicted;     // buffer to hold the predicted displacements
};

// the implementations of the inline methods
#define altar_models_cudamogi_Source_icc
#include "Source.icc"
#undef altar_models_cudamogi_Source_icc

// code guard
#endif

// end of file
