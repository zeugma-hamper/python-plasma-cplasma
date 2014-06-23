
// (c) 2014 MCT

#pragma once

// Macros to make Python Plasma bindings a little less tedious

// Handy function for turning some pack of preprocessor nonsense in to a string
#define STR(X) #X

// Check the retort of an expression. Is it not splend? Throw it.
#define THROW_ERROR_TORT(expr) do {             \
    ob_retort tort = expr;                      \
    if (0 > tort) {                             \
      throw PlasmaException (tort);             \
    }                                           \
  } while (false)


// For each int type, with an optional prefix, run a macro
// with the type as its sole argument
#define DECLARE_INTS(M, PRE)                         \
  M(PRE##unt8)                                       \
  M(PRE##int8)                                       \
  M(PRE##unt16)                                      \
  M(PRE##int16)                                      \
  M(PRE##unt32)                                      \
  M(PRE##int32)                                      \
  M(PRE##unt64)                                      \
  M(PRE##int64)

// For each float type with an optional prefix, run a macro
// with the type as its sole argument
#define DECLARE_FLOATS(M, PRE)                  \
  M(PRE##float32)                               \
  M(PRE##float64)

// For each int type with an optional prefix, run a macro
// with the type and a slaw `s` as its arguments
#define FOR_ALL_INTS(M, PRE, s)                 \
  M (PRE ## unt8, s);                           \
  M (PRE ## int8, s);                           \
  M (PRE ## unt16, s);                          \
  M (PRE ## int16, s);                          \
  M (PRE ## unt32, s);                          \
  M (PRE ## int32, s);                          \
  M (PRE ## unt64, s);                          \
  M (PRE ## int64, s);

// For each float type with an optional prefix, run a macro
// with the type and a slaw `s` as its arguments
#define FOR_ALL_FLOATS(M, PRE, s)               \
  M (PRE ## float32, s);                        \
  M (PRE ## float64, s);

// Check to see if we're a certain numeric type.
// If we are, return that type.
#define RETURN_IF_NUMERIC(TYP, s) do {          \
    if (slaw_is_ ## TYP (s)) {                  \
      const TYP *tmp;                           \
      tmp = slaw_ ## TYP ## _emit (s);          \
      return py::object (*tmp);                 \
      }                                         \
  } while (false)

// Check to see if we're a numeric array. of a certain type.
// If so, marshal that data in to a numpy array.
#define RETURN_IF_NUMARRAY(TYP, s) do {                          \
    if (slaw_is_ ## TYP ## _array (s)) {                         \
      const TYP *tmp = slaw_ ## TYP ## _array_emit (s);          \
      const int64 N = slaw_numeric_array_count (s);              \
      return detail::makeNumpyArray<TYP>(tmp, N);                \
    }                                                            \
  } while (false)

// Create a struct specialization to tell us everything we need
// to know about marshaling from slaw arrays to numpy arrays
#define DECLARE_NUMPY_INFO(T, NT, DIMS)                         \
  template <> struct numpy_info<T> {                            \
    static const int typenum() { return NT; }                   \
    static const int ND() { return  DIMS > 1 ? 2 : 1; }         \
    static std::vector<npy_intp> Dims (int64 len) {             \
      std::vector<npy_intp> out = { npy_intp(len) };            \
      if (DIMS > 1) {                                           \
        out . push_back (DIMS);                                 \
      }                                                         \
      return out;                                               \
    }                                                           \
  }

// Per-numeric-type methods to create new slaw
#define SLAW_FROM_NUMERIC(T)                                    \
  static Ref make_ ## T (T t) {                                 \
    fprintf (stderr, "Slaw::" STR(make_ ## T) "\n");            \
    return Ref(new Slaw (slaw_##T (t)));                        \
  }

// Per-numeric-type methods to create new slaw
#define SLAW_FROM_NUMERICV(T)                                   \
  static Ref make_ ## T (py::object obj) {                      \
    py::extract<T> vec (obj);                                   \
    if (! vec . check ()) {                                     \
      throw PlasmaException (SLAW_NOT_NUMERIC);                 \
    }                                                           \
    return Ref (new Slaw (slaw_##T (vec ())));                  \
  }

// Define endpoints in the Slaw python class.
// Note that the names here are make_whatever rather than
// the conventional makeWhatever. This is because it would
// be a lot of work to make the preprocessor know that for
// each unt8 it wants to call it Uint8 in these circumstantes.
// (Though I'll note that it would be easy if we were working
// in the D programming language.)
#define DECLARE_SLAW_FROM(T)                        \
  .def("make", &Slaw::make_ ##T)                    \
  .def(STR(make_ ## T), &Slaw::make_ ##T)           \
  .staticmethod(STR(make_ ## T))

// Vector types don't get the raw "make" on account of
// they take just an object and will stomp all the other
// signatures.
#define DECLARE_SLAW_FROMV(T)                       \
  .def(STR(make_ ## T), &Slaw::make_ ##T)           \
  .staticmethod(STR(make_ ## T))

// Given a numeric type and assuming a numpy array with 1 dimension,
// create a slaw from its data if indeed the type matches.
#define NPYARR_SINGLE(NPYTYP, OBTYP)                            \
  if (typ == NPYTYP) {                                          \
    OBTYP* data = reinterpret_cast<OBTYP*> (buffer);            \
    return Ref(new Slaw (slaw_##OBTYP##_array(data, len)));     \
  }

// Given a numeric type and assuming a numpy array with 2 dimensions,
// the first of size two, create a slaw from its data if indeed the
// type matches.
#define NPYARR_DOUBLE(NPYTYP, OBTYP)                                    \
  if (typ == NPYTYP) {                                                  \
    v2##OBTYP* data = reinterpret_cast<v2##OBTYP*> (buffer);            \
        return Ref(new Slaw (slaw_v2##OBTYP##_array(data, len)));       \
  }

// Given a numeric type and assuming a numpy array with 2 dimensions,
// the first of size three, create a slaw from its data if indeed the
// type matches.
#define NPYARR_TRIPLE(NPYTYP, OBTYP)                                    \
  if (typ == NPYTYP) {                                                  \
    v3##OBTYP* data = reinterpret_cast<v3##OBTYP*> (buffer);            \
        return Ref(new Slaw (slaw_v3##OBTYP##_array(data, len)));       \
  }

// Given a numeric type and assuming a numpy array with 2 dimensions,
// the first of size four, create a slaw from its data if indeed the
// type matches.
#define NPYARR_QUAD(NPYTYP, OBTYP)                                      \
  if (typ == NPYTYP) {                                                  \
    v4##OBTYP* data = reinterpret_cast<v4##OBTYP*> (buffer);            \
        return Ref(new Slaw (slaw_v4##OBTYP##_array(data, len)));       \
  }

// Declare types to take ob-vectors to/from numpy.ndarrays
#define DECLARE_VECT_CONVERTER(TYP, VSIZE, NPYTYP)                      \
    typedef vtype_to_python_obj<v##VSIZE##TYP, VSIZE, NPYTYP>           \
    v##VSIZE##TYP##_converter;                                          \
    typedef python_obj_to_vtype<v##VSIZE##TYP, TYP, VSIZE, NPYTYP>      \
    v##VSIZE##TYP##_extractor;

// Register types to take ob-vectors to/from numpy.ndarrays
#define REGISTER_VECT_CONVERTER(TYP, VSIZE, NPYTYP)              \
    py::to_python_converter                                      \
    <v##VSIZE##TYP, detail::v##VSIZE##TYP##_converter> ();       \
    py::converter::registry::push_back(                          \
        &detail::v##VSIZE##TYP##_extractor::convertible,         \
        &detail::v##VSIZE##TYP##_extractor::construct,           \
      py::type_id<v##VSIZE##TYP>())

