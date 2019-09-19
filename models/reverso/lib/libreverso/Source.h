// -*- C++ -*-
//
// eric m. gurrola  <eric.m.gurrola@jpl.nasa.gov>
// (c) 2019 california institute of technology * jet propulsion lab * nasa
// all rights reserved
//

// code guard
#if !defined(altar_models_reverso_Source_h)
#define altar_models_reverso_Source_h

// external
#include <vector>

// forward declarations
namespace altar {
    namespace models {
        namespace reverso {
            // forwards declarations
            class Source;

            // type aliases
            using source_t = Source;
        }
    }
}


// the reverso source
class altar::models::reverso::Source {
    // types
public:
    using size_type = std::size_t;
    using oids_type = std::vector<std::size_t>;

    // meta-methods
public:
    virtual ~Source();
    inline explicit Source(double g, double Gsm, double nu, double mu, double drho);

    // interface
public:
    inline void data(gsl_vector * data);
    inline void locations(gsl_matrix * locations);
    inline void los(gsl_matrix * los);
    inline void oids(const oids_type & oids);
    inline void layout(size_type asIdx, size_type adIdx,
                       size_type acIdx, size_type hsIdx, size_type hdIdx,
                       size_type qIdx);

    void displacements(gsl_matrix_view * samples, gsl_matrix * predicted) const;
    void residuals(gsl_matrix * predicted) const;

    // implementation details
private:
    gsl_vector * _data;        // borrowed reference
    gsl_matrix * _locations;   // owned
    gsl_matrix * _los;         // owned
    oids_type _oids;           // owned

    // Gravitational acceleration [m/s**2], value = 9.8 at sea level
    double _g;
    // Material properties
    // the shear modulus [kg/(m*s**2)], nominal value = 20.0e9
    double _Gsm;
    // the Poisson ratio (dimensionless)
    double _nu;
    // Viscosity [kg/(m*s)], nominal value = 2000.0
    double _mu;
    // Density Difference (ρ_r - ρ_m), [kg/m**3] (density_rock - density_magma) , nominal value 300
    double _drho;

    // the layout of the various parameters within a sample
    //
    // (x0, y0, z0=0) = coordinates of the projection of the center of the pipe
    // connecting the two reservoirs onto the planar earth surface.
    // (z0 = 0 at the local tangent plane of the earth's surface.)
    size_type _x0Idx;
    size_type _y0Idx;
    // time origin of the beginning of the magma flow
    size_type _t0Idx;
    // radius of the shallow reservoir (circular sill)
    size_type _asIdx;
    // depth of the shallow reservoir
    size_type _hsIdx;
    // radius of the connecting pipe between the two reservoirs
    size_type _acIdx;
    // radius of the deep reservoir (circular sill)
    size_type _adIdx;
    // depth of the deep reservoir
    size_type _hdIdx;
    // base magma inflow rate
    size_type _qIdx;
};

// the implementations of the inline methods
#define altar_models_reverso_Source_icc
#include "Source.icc"
#undef altar_models_reverso_Source_icc

// code guard
#endif

// end of file
