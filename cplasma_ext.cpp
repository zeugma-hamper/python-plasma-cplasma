
// (c) 2014 MCT

#include <iostream>

#include <libPlasma/c/pool.h>
#include <libPlasma/c/protein.h>
#include <libPlasma/c/slaw.h>
#include <libPlasma/c/slaw-io.h>

#include <boost/python.hpp>
#include <boost/shared_ptr.hpp>
#include <numpy/ndarrayobject.h> 

#include <string>
#include <vector>
#include <locale>
#include <codecvt>

#include <fcntl.h>

#include "horrible_macros.hpp"


namespace py = boost::python;

const std::string fromwstr(const std::wstring& s) {
    std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>> converter;
    return converter.to_bytes(s);
}

class PlasmaException : public std::exception {
 private:
  ob_retort tort;

 public:
  PlasmaException(ob_retort t)  :  tort { t } {}

  const char* description() const { return ob_error_string (tort); }
  const ob_retort retort() const { return tort; }
};

template <typename T> struct array_writer {};

namespace detail {

// numpy info.  For each ob numeric type, there's a corresponding
// specialization of the numpy_info<> struct that has one const
// and two functions:
// - typenum: the numpy type identifier that corresponds to the ob type
// - ND(), which returns the number of dimensions the array shall have
// - Dims (), which returns an array describing these dimensions in
//   numpy's preferred format.

template <typename T> struct numpy_info { };


// Numeric conversion types of vNtypeBits types.
// Convert to python objects (numpy.ndarray)
template <typename V, int VSIZE, int NPYTYP>
struct vtype_to_python_obj {
  static PyObject* convert (V const& v) {
    npy_intp dim = VSIZE;
    // Yes, we're treating the vector type as an array. Intentionally.
    PyObject* src = PyArray_SimpleNewFromData
        (1, &dim, NPYTYP, (void*) &v);
    PyObject* arr = PyArray_EMPTY(1, &dim, NPYTYP, 0);
    PyArray_CopyInto (reinterpret_cast<PyArrayObject*> (arr),
                      reinterpret_cast<PyArrayObject*> (src));
    return py::incref(arr);
  }
};
// Convert from python objects (numpy.ndarray)
template <typename V, typename T, int VSIZE, int NPYTYP>
struct python_obj_to_vtype {
  static void* convertible(PyObject* objptr) {
    if (NPYTYP == PyArray_TYPE(objptr)) {
      py::handle<> h (py::borrowed (objptr));
      py::object arr(h);
      py::object shape = arr.attr ("shape");
      if (1 == py::len (shape) && VSIZE == py::extract<int> (shape[0])) {
        return objptr;
      }
    }
    return nullptr;
  }
  
  // Convert obj_ptr into a QString
  static void construct(
      PyObject* obj_ptr,
      boost::python::converter::rvalue_from_python_stage1_data* data)
  { void* orig = ((PyArrayObject*) obj_ptr) -> data;
    // Grab pointer to memory into which to construct the new QString
    void* storage = (
        (boost::python::converter::rvalue_from_python_storage<V>*)
        data)->storage.bytes;
    // It's all just packed arrays, right? What could possibly go wrong?
    memcpy(storage, orig, VSIZE * sizeof(T));
    // Stash the memory chunk pointer for later use by boost.python
    data->convertible = storage;
  }
};

// Template definitions for converting from slaw arrays to numpy arrays
DECLARE_NUMPY_INFO(unt8, NPY_UINT8, 1);
DECLARE_NUMPY_INFO(int8, NPY_INT8, 1);
DECLARE_NUMPY_INFO(unt16, NPY_UINT16, 1);
DECLARE_NUMPY_INFO(int16, NPY_INT16, 1);
DECLARE_NUMPY_INFO(unt32, NPY_UINT32, 1);
DECLARE_NUMPY_INFO(int32, NPY_INT32, 1);
DECLARE_NUMPY_INFO(unt64, NPY_UINT64, 1);
DECLARE_NUMPY_INFO(int64, NPY_INT64, 1);
DECLARE_NUMPY_INFO(float32, NPY_FLOAT32, 1);
DECLARE_NUMPY_INFO(float64, NPY_FLOAT64, 1);

DECLARE_NUMPY_INFO(v2unt8, NPY_UINT8, 2);
DECLARE_NUMPY_INFO(v2int8, NPY_INT8, 2);
DECLARE_NUMPY_INFO(v2unt16, NPY_UINT16, 2);
DECLARE_NUMPY_INFO(v2int16, NPY_INT16, 2);
DECLARE_NUMPY_INFO(v2unt32, NPY_UINT32, 2);
DECLARE_NUMPY_INFO(v2int32, NPY_INT32, 2);
DECLARE_NUMPY_INFO(v2unt64, NPY_UINT64, 2);
DECLARE_NUMPY_INFO(v2int64, NPY_INT64, 2);
DECLARE_NUMPY_INFO(v2float32, NPY_FLOAT32, 2);
DECLARE_NUMPY_INFO(v2float64, NPY_FLOAT64, 2);

DECLARE_NUMPY_INFO(v3unt8, NPY_UINT8, 3);
DECLARE_NUMPY_INFO(v3int8, NPY_INT8, 3);
DECLARE_NUMPY_INFO(v3unt16, NPY_UINT16, 3);
DECLARE_NUMPY_INFO(v3int16, NPY_INT16, 3);
DECLARE_NUMPY_INFO(v3unt32, NPY_UINT32, 3);
DECLARE_NUMPY_INFO(v3int32, NPY_INT32, 3);
DECLARE_NUMPY_INFO(v3unt64, NPY_UINT64, 3);
DECLARE_NUMPY_INFO(v3int64, NPY_INT64, 3);
DECLARE_NUMPY_INFO(v3float32, NPY_FLOAT32, 3);
DECLARE_NUMPY_INFO(v3float64, NPY_FLOAT64, 3);

DECLARE_NUMPY_INFO(v4unt8, NPY_UINT8, 4);
DECLARE_NUMPY_INFO(v4int8, NPY_INT8, 4);
DECLARE_NUMPY_INFO(v4unt16, NPY_UINT16, 4);
DECLARE_NUMPY_INFO(v4int16, NPY_INT16, 4);
DECLARE_NUMPY_INFO(v4unt32, NPY_UINT32, 4);
DECLARE_NUMPY_INFO(v4int32, NPY_INT32, 4);
DECLARE_NUMPY_INFO(v4unt64, NPY_UINT64, 4);
DECLARE_NUMPY_INFO(v4int64, NPY_INT64, 4);
DECLARE_NUMPY_INFO(v4float32, NPY_FLOAT32, 4);
DECLARE_NUMPY_INFO(v4float64, NPY_FLOAT64, 4);

// Template definitions for convertion from vNtypeBITs to numpy arrays
DECLARE_VECT_CONVERTER(unt8, 2, NPY_UINT8);
DECLARE_VECT_CONVERTER(int8, 2, NPY_INT8);
DECLARE_VECT_CONVERTER(unt16, 2, NPY_UINT16);
DECLARE_VECT_CONVERTER(int16, 2, NPY_INT16);
DECLARE_VECT_CONVERTER(unt32, 2, NPY_UINT32);
DECLARE_VECT_CONVERTER(int32, 2, NPY_INT32);
DECLARE_VECT_CONVERTER(unt64, 2, NPY_UINT64);
DECLARE_VECT_CONVERTER(int64, 2, NPY_INT64);
DECLARE_VECT_CONVERTER(float32, 2, NPY_FLOAT32);
DECLARE_VECT_CONVERTER(float64, 2, NPY_FLOAT64);

DECLARE_VECT_CONVERTER(unt8, 3, NPY_UINT8);
DECLARE_VECT_CONVERTER(int8, 3, NPY_INT8);
DECLARE_VECT_CONVERTER(unt16, 3, NPY_UINT16);
DECLARE_VECT_CONVERTER(int16, 3, NPY_INT16);
DECLARE_VECT_CONVERTER(unt32, 3, NPY_UINT32);
DECLARE_VECT_CONVERTER(int32, 3, NPY_INT32);
DECLARE_VECT_CONVERTER(unt64, 3, NPY_UINT64);
DECLARE_VECT_CONVERTER(int64, 3, NPY_INT64);
DECLARE_VECT_CONVERTER(float32, 3, NPY_FLOAT32);
DECLARE_VECT_CONVERTER(float64, 3, NPY_FLOAT64);

DECLARE_VECT_CONVERTER(unt8, 4, NPY_UINT8);
DECLARE_VECT_CONVERTER(int8, 4, NPY_INT8);
DECLARE_VECT_CONVERTER(unt16, 4, NPY_UINT16);
DECLARE_VECT_CONVERTER(int16, 4, NPY_INT16);
DECLARE_VECT_CONVERTER(unt32, 4, NPY_UINT32);
DECLARE_VECT_CONVERTER(int32, 4, NPY_INT32);
DECLARE_VECT_CONVERTER(unt64, 4, NPY_UINT64);
DECLARE_VECT_CONVERTER(int64, 4, NPY_INT64);
DECLARE_VECT_CONVERTER(float32, 4, NPY_FLOAT32);
DECLARE_VECT_CONVERTER(float64, 4, NPY_FLOAT64);

template <typename T>
py::object makeNumpyArray (const T* data, int64 len) {
  std::vector<npy_intp> dims = detail::numpy_info<T>::Dims (len);
  int nd = numpy_info<T>::ND ();
  int typenum = numpy_info<T>::typenum ();
  PyObject* src = PyArray_SimpleNewFromData
      (nd, &dims[0], typenum, (void*) data);
  py::handle<> mort (src);
  PyObject* arr_ = PyArray_EMPTY (nd, &dims[0], typenum, 0);
  PyArray_CopyInto (reinterpret_cast<PyArrayObject*>(arr_),
                    reinterpret_cast<PyArrayObject*>(src));  
  py::handle<> h(arr_);
  py::object arr(h);
  return arr;
}

} // end detail

class Slaw;

class BSlaw {
 private:
  bslaw slaw_;

 public:
  BSlaw (bslaw s) : slaw_ { s } {}

  slaw dup () { return slaw_dup (slaw_); }
  bslaw peek () const { return slaw_; }

  std::string toYaml() {
    slaw s;
    ob_retort tort = slaw_to_string (slaw_, &s);
    if (0 > tort) {
      throw PlasmaException (tort);
    }
    std::string output(slaw_string_emit(s));
    slaw_free(s);
    return output;
  }

  py::object emit_list () const {
    py::list lst;
    bslaw s = slaw_list_emit_first (slaw_);
    while (s != NULL) {
      BSlaw tmp { s };
      lst . append (tmp . emit ());
      s = slaw_list_emit_next (slaw_, s);
    }
    return lst;
  }

  py::object emit_map () const { 
    py::object collections = py::import("collections");
    py::object od_class = collections.attr("OrderedDict");
    py::object dct = od_class();
    py::object set_default = dct.attr("setdefault");
    bslaw s = slaw_list_emit_first (slaw_);
    while (s != NULL) {
      BSlaw car { slaw_cons_emit_car (s) };
      BSlaw cdr { slaw_cons_emit_cdr (s) };
      set_default (car.emit(), cdr.emit());
      s = slaw_list_emit_next (slaw_, s);
    }
    return dct;
  }

  py::object emit_cons () const {
    BSlaw car { slaw_cons_emit_car (slaw_) };
    BSlaw cdr { slaw_cons_emit_cdr (slaw_) };
    return py::make_tuple (car . emit (), cdr . emit ());
  }

  py::object emit_numeric_vector_array () const {
    FOR_ALL_INTS(RETURN_IF_NUMARRAY,v2,slaw_);
    FOR_ALL_FLOATS(RETURN_IF_NUMARRAY,v2,slaw_);
    FOR_ALL_INTS(RETURN_IF_NUMARRAY,v3,slaw_);
    FOR_ALL_FLOATS(RETURN_IF_NUMARRAY,v3,slaw_);
    FOR_ALL_INTS(RETURN_IF_NUMARRAY,v4,slaw_);
    FOR_ALL_FLOATS(RETURN_IF_NUMARRAY,v4,slaw_);
    return py::object();
  }

  py::object emit_numeric_vector () const {
    FOR_ALL_INTS(RETURN_IF_NUMERIC, v2, slaw_);
    FOR_ALL_FLOATS(RETURN_IF_NUMERIC, v2, slaw_);
    FOR_ALL_INTS(RETURN_IF_NUMERIC, v3, slaw_);
    FOR_ALL_FLOATS(RETURN_IF_NUMERIC, v3, slaw_);
    FOR_ALL_INTS(RETURN_IF_NUMERIC, v4, slaw_);
    FOR_ALL_FLOATS(RETURN_IF_NUMERIC, v4, slaw_);
    return py::object();
  }

  py::object emit_numeric_array () const { 
    FOR_ALL_INTS(RETURN_IF_NUMARRAY,,slaw_);
    FOR_ALL_FLOATS(RETURN_IF_NUMARRAY,,slaw_);
    return py::object();
  }

  py::object emit_numeric () const { 
    FOR_ALL_INTS(RETURN_IF_NUMERIC,,slaw_);
    FOR_ALL_FLOATS(RETURN_IF_NUMERIC,,slaw_);
    return py::object();
  }

  py::object emit () const; 
  unt64 listCount () const {
    return slaw_list_count (slaw_);
  }

  BSlaw nth(int64 n) const {
    return BSlaw (slaw_list_emit_nth (slaw_, n));
  }

  bool isProtein() const { return slaw_is_protein (slaw_); }

  BSlaw descrips() const {
    if (! slaw_is_protein (slaw_)) {
      throw PlasmaException (POOL_NOT_A_PROTEIN);
    }
    return BSlaw (protein_descrips(slaw_));
  }

  BSlaw ingests() const {
    if (! slaw_is_protein (slaw_)) {
      throw PlasmaException (POOL_NOT_A_PROTEIN);
    }
    return BSlaw (protein_ingests (slaw_));
  }

  int64 listFind (int64) const;
  BSlaw mapFind (boost::shared_ptr<Slaw>) const;

  int64 gapsearch (BSlaw search) const {
    return slaw_list_gapsearch (slaw_, search . peek ());
  }
};


class BProtein {
 private:
  bprotein pro;

 public:
  BProtein (bprotein p) : pro { p } {}
  BSlaw ingests () const { return BSlaw (protein_ingests (pro)); }
  BSlaw descrips () const { return BSlaw (protein_descrips (pro)); }

  protein dup () { return protein_dup (pro); }

  py::object emit () const {
    py::dict dct;
    dct.setdefault("descrips", descrips () . emit ());
    dct.setdefault("ingests", ingests () . emit ());
    return dct;
  }

  std::string toYaml() {
    slaw s;
    ob_retort tort = slaw_to_string (pro, &s);
    if (0 > tort) {
      throw PlasmaException (tort);
    }
    std::string output(slaw_string_emit(s));
    slaw_free(s);
    return output;
  }
};


py::object BSlaw::emit () const {
  if (slaw_is_protein (slaw_)) {
    return BProtein(slaw_).emit();
  } else if (slaw_is_list (slaw_)) {
    return emit_list ();
  } else if (slaw_is_map (slaw_)) {
    return emit_map ();
  } else if (slaw_is_cons (slaw_)) {
    return emit_cons ();
  } else if (slaw_is_numeric_vector (slaw_)) {
    if (slaw_is_numeric_array (slaw_)) {
      return emit_numeric_vector_array ();
    } else { 
      return emit_numeric_vector ();
    }
  } else if (slaw_is_numeric_array (slaw_)) {
    return emit_numeric_array ();
  } else if (slaw_is_numeric (slaw_)) {
    return emit_numeric ();
  } else if (slaw_is_nil (slaw_)) { 
    return py::object ();
  } else if (slaw_is_string (slaw_)) {
    return py::object (slaw_string_emit (slaw_));
  } else if (slaw_is_boolean (slaw_)) {
    return py::object (bool(*slaw_boolean_emit (slaw_)));
  } else {
    return py::object ();
  }
}


class Slaw {
 private:
  slaw slaw_;

 public:
  typedef boost::shared_ptr<Slaw> Ref;
  Slaw () = default;
  Slaw (slaw s) : slaw_ { s } {
    assert(nullptr != s);
  }

  ~Slaw () {
    if (nullptr != slaw_) {
      slaw_free (slaw_);
      slaw_ = nullptr;
    }
  }

  slaw take () { 
    slaw out = slaw_;
    slaw_ = nullptr;
    return out;
  }

  bslaw peek () const {
    return slaw_;
  }

  std::string toYaml() {
    slaw s;
    ob_retort tort = slaw_to_string (slaw_, &s);
    if (0 > tort) {
      throw PlasmaException (tort);
    }
    std::string output(slaw_string_emit(s));
    slaw_free(s);
    return output;
  }

  static Ref fromYaml (std::string yaml) {
    slaw s;
    ob_retort tort = slaw_from_string (yaml.c_str(), &s);
    if (tort < 0) {
      throw PlasmaException (tort);
    }
    return Ref(new Slaw (s));
  }
  static Ref fromYamlW (std::wstring yaml) {
    return fromYaml (fromwstr (yaml));
  }

  static py::list fromFileGeneric(slaw_input input) {
    slaw s;
    py::list output;
    ob_retort tort = slaw_input_read (input, &s);
    while (OB_OK == tort) {
      output.append(Ref (new Slaw (s)));
      tort = slaw_input_read (input, &s);
    }
    slaw_input_close (input);
    if (SLAW_END_OF_FILE != tort) {
      throw PlasmaException (tort);
    }
    return output;
  }
  
  static py::list fromFile (std::string filename) {
    slaw_input input;
    int fd = open(filename . c_str(), O_RDONLY);
    if (-1 == fd) {
      throw PlasmaException (OB_NOT_FOUND);
    }
    ob_retort tort = slaw_input_open_text_fdx(fd, &input);
    if (0 > tort) {
      slaw_input_close (input);
      throw PlasmaException (tort);
    }
    return fromFileGeneric (input);
  }

  static py::list fromFileBinary (std::string filename) {
    slaw_input input;
    int fd = open(filename . c_str(), O_RDONLY);
    if (-1 == fd) {
      throw PlasmaException (OB_NOT_FOUND);
    }
    ob_retort tort = slaw_input_open_binary_fdx(fd, &input);
    if (0 > tort) {
      slaw_input_close (input);
      throw PlasmaException (tort);
    }
    return fromFileGeneric (input);
  }

  static Ref fromBslaw (BSlaw bs) {
    return Ref(new Slaw (bs.dup()));
  }

  static Ref fromBprotein (BProtein bp) {
    return Ref (new Slaw (bp.dup()));
  }

  static Ref from_string (std::string s) {
    return Ref(new Slaw (slaw_string (s.c_str())));
  }

  static Ref from_stringW (std::wstring s) {
    return from_string (fromwstr (s));
  }

  static Ref makeCons (Ref car, Ref cdr) {
    return Ref (new Slaw (slaw_cons_ff (car -> take (),
                                        cdr -> take ())));
  }
  
  DECLARE_INTS (SLAW_FROM_NUMERIC,);
  DECLARE_FLOATS (SLAW_FROM_NUMERIC,);

  DECLARE_INTS (SLAW_FROM_NUMERICV, v2);
  DECLARE_FLOATS (SLAW_FROM_NUMERICV, v2);

  DECLARE_INTS (SLAW_FROM_NUMERICV, v3);
  DECLARE_FLOATS (SLAW_FROM_NUMERICV, v3);

  DECLARE_INTS (SLAW_FROM_NUMERICV, v4);
  DECLARE_FLOATS (SLAW_FROM_NUMERICV, v4);

  static Ref nil() { return Ref (new Slaw (slaw_nil())); }
  
  static Ref from_obj(py::object &obj) {
    if (obj . is_none ()) {
      return nil();
    }
    throw PlasmaException (SLAW_FABRICATOR_BADNESS);
  }


  static Ref _from_numpy(const py::numeric::array& arr, size_t len) {
    const int typ = PyArray_TYPE(arr.ptr());
    void * buffer = PyArray_GETPTR1(arr.ptr(), 0);

    NPYARR_SINGLE(NPY_UINT8, unt8);
    NPYARR_SINGLE(NPY_INT8, int8);

    NPYARR_SINGLE(NPY_UINT16, unt16);
    NPYARR_SINGLE(NPY_INT16, int16);

    NPYARR_SINGLE(NPY_UINT32, unt32);
    NPYARR_SINGLE(NPY_INT32, int32);

    NPYARR_SINGLE(NPY_UINT64, unt64);
    NPYARR_SINGLE(NPY_INT64, int64);

    NPYARR_SINGLE(NPY_FLOAT32, float32);
    NPYARR_SINGLE(NPY_FLOAT64, float64);

    throw PlasmaException (SLAW_FABRICATOR_BADNESS);
  }

  static Ref _from_numpy(const py::numeric::array& arr, size_t len, size_t vsize) {
    const int typ = PyArray_TYPE(arr.ptr());
    void * buffer = PyArray_GETPTR1(arr.ptr(), 0);

    if (2 == vsize) {
      NPYARR_DOUBLE(NPY_UINT8, unt8);
      NPYARR_DOUBLE(NPY_INT8, int8);

      NPYARR_DOUBLE(NPY_UINT16, unt16);
      NPYARR_DOUBLE(NPY_INT16, int16);

      NPYARR_DOUBLE(NPY_UINT32, unt32);
      NPYARR_DOUBLE(NPY_INT32, int32);

      NPYARR_DOUBLE(NPY_UINT64, unt64);
      NPYARR_DOUBLE(NPY_INT64, int64);

      NPYARR_DOUBLE(NPY_FLOAT32, float32);
      NPYARR_DOUBLE(NPY_FLOAT64, float64);
    }
    if (3 == vsize) {
      NPYARR_TRIPLE(NPY_UINT8, unt8);
      NPYARR_TRIPLE(NPY_INT8, int8);

      NPYARR_TRIPLE(NPY_UINT16, unt16);
      NPYARR_TRIPLE(NPY_INT16, int16);

      NPYARR_TRIPLE(NPY_UINT32, unt32);
      NPYARR_TRIPLE(NPY_INT32, int32);

      NPYARR_TRIPLE(NPY_UINT64, unt64);
      NPYARR_TRIPLE(NPY_INT64, int64);

      NPYARR_TRIPLE(NPY_FLOAT32, float32);
      NPYARR_TRIPLE(NPY_FLOAT64, float64);
    }
    if (4 == vsize) {
      NPYARR_QUAD(NPY_UINT8, unt8);
      NPYARR_QUAD(NPY_INT8, int8);

      NPYARR_QUAD(NPY_UINT16, unt16);
      NPYARR_QUAD(NPY_INT16, int16);

      NPYARR_QUAD(NPY_UINT32, unt32);
      NPYARR_QUAD(NPY_INT32, int32);

      NPYARR_QUAD(NPY_UINT64, unt64);
      NPYARR_QUAD(NPY_INT64, int64);

      NPYARR_QUAD(NPY_FLOAT32, float32);
      NPYARR_QUAD(NPY_FLOAT64, float64);
    }

    throw PlasmaException (SLAW_FABRICATOR_BADNESS);
  }

  static Ref from_numpy(const py::numeric::array& arr) {
    py::object shape = arr.attr("shape");
    auto shape_len = py::len (shape);
    if (1 == shape_len) { // simple array
      return _from_numpy (arr, py::extract<size_t> (shape[0]));
    } else if (2 == shape_len) { // vNtype
      return _from_numpy (arr,
                          py::extract<size_t> (shape[0]),
                          py::extract<size_t> (shape[1]));
    } 
    throw PlasmaException (SLAW_FABRICATOR_BADNESS);
  }
  
  BSlaw read () { return BSlaw (slaw_); }

  bool isProtein() const { return slaw_is_protein (slaw_); }

  BSlaw descrips() const {
    if (! slaw_is_protein (slaw_)) {
      throw PlasmaException (POOL_NOT_A_PROTEIN);
    }
    return BSlaw (protein_descrips(slaw_));
  }

  BSlaw ingests() const {
    if (! slaw_is_protein (slaw_)) {
      throw PlasmaException (POOL_NOT_A_PROTEIN);
    }
    return BSlaw (protein_ingests (slaw_));
  }

  static Ref makeProtein (Ref des, Ref ing) {
    return Ref(new Slaw (protein_from_ff(des -> take (),
                                         ing -> take ())));
  }
};

int64 BSlaw::listFind (int64 x) const {
  auto val = Slaw::make_int64 (x);
  return slaw_list_find (slaw_, val -> peek ());
}

BSlaw BSlaw::mapFind (boost::shared_ptr<Slaw> val) const {
  return BSlaw (slaw_map_find (slaw_, val -> peek ()));
}


class SlawBuilder {
 private:
  slabu* bu_;

 public:
  typedef boost::shared_ptr<SlawBuilder> Ref;

  SlawBuilder () {
    bu_ = slabu_new ();
  }

  ~SlawBuilder () {
    if (nullptr != bu_) {
      slabu_free (bu_);
    }
  }

  Slaw::Ref takeList () {
    slaw s = slaw_list_f (bu_);
    bu_ = slabu_new();
    return Slaw::Ref (new Slaw (s));
  }

  Slaw::Ref takeMap () {
    slaw s = slaw_map_f (bu_);
    bu_ = slabu_new ();
    return Slaw::Ref (new Slaw (s));
  }

  void listAppend(Slaw::Ref s) {
    THROW_ERROR_TORT (slabu_list_add_f (bu_, s -> take ()));
  }

  void mapPut(Slaw::Ref k, Slaw::Ref v) {
    THROW_ERROR_TORT (slabu_map_put_ff (bu_,
                                        k -> take (),
                                        v -> take ()));
  }
};

class Hose {
 private:
  pool_hose hose;

  void Init (std::string pool) {
    ob_retort tort = pool_participate (pool . c_str (),
                                       &hose,
                                       nullptr);
    if (0 > tort) {
      hose = nullptr; // belt, suspenders
      throw PlasmaException (tort);
    }
  }
 public:
  Hose (std::string pool) : hose { nullptr } {
    Init (pool);
  }

  Hose (std::wstring pool) : hose { nullptr } {
    Init (fromwstr(pool));
  }


  virtual ~Hose () {
    if (nullptr != hose) {
      pool_withdraw (hose);
    }
  }

  void enableWakeup () {
    THROW_ERROR_TORT(pool_hose_enable_wakeup (hose));
  }

  pool_hose peek () const { return hose; }

  static void create(std::string name,
                     std::string type,
                     const Slaw& options) {
    THROW_ERROR_TORT(pool_create (name . c_str (),
                                  type . c_str (),
                                  options . peek()));
  }

  static void dispose(std::string name) {
    THROW_ERROR_TORT(pool_dispose (name . c_str ()));
  }

  static void rename (std::string old_name, std::string new_name) {
    THROW_ERROR_TORT (pool_rename (old_name . c_str (),
                                   new_name . c_str ()));
  }

  static bool exists (std::string name) {
    return OB_YES == pool_exists (name . c_str ());
  }

  static bool validateName (std::string name) {
    return OB_OK == pool_validate_name (name . c_str ());
  }

  static void sleep (std::string name) {
    THROW_ERROR_TORT (pool_sleep (name . c_str ()));
  }

  static bool checkInUse(std::string name) {
    return POOL_IN_USE == pool_check_in_use (name . c_str ());
  }

  static py::object listPools () {
    slaw s;
    THROW_ERROR_TORT (pool_list (&s));
    py::object out = BSlaw (s) . emit ();
    slaw_free (s);
    return out;
  }

  static py::object listPoolsEx(std::string prefix) {
    slaw s;
    THROW_ERROR_TORT (pool_list_ex (prefix . c_str (), &s));
    py::object out = BSlaw (s) . emit ();
    slaw_free (s);
    return out;
  }    
  
  const char* name() const {
    return pool_name (hose);
  }

  const char* hoseName() const {
    return pool_get_hose_name (hose);
  }

  void setHoseName (std::string str) {
    THROW_ERROR_TORT (pool_set_hose_name (hose, str . c_str ()));
  }

  BProtein getInfo (int64 hops) {
    protein pro;
    THROW_ERROR_TORT (pool_get_info (hose, hops, &pro));
    return BProtein (pro);
  }

  int64 newestIndex() const {
    int64 out;
    THROW_ERROR_TORT(pool_newest_index(hose, &out));
    return out;
  }

  int64 oldestIndex() const {
    int64 out;
    THROW_ERROR_TORT(pool_oldest_index(hose, &out));
    return out;
  }

  int64 index() const {
    int64 out;
    THROW_ERROR_TORT(pool_index (hose, &out));
    return out;
  }

  void rewind() { THROW_ERROR_TORT(pool_rewind (hose)); }
  void tolast() { THROW_ERROR_TORT(pool_tolast (hose)); }
  void runout() { THROW_ERROR_TORT(pool_runout (hose)); }

  void frwdby(int64 indoff) { THROW_ERROR_TORT(pool_frwdby (hose, indoff)); }
  void backby(int64 indoff) { THROW_ERROR_TORT(pool_backby (hose, indoff)); }
  void seekto(int64 idx) { THROW_ERROR_TORT(pool_seekto (hose, idx)); }

  void wakeup() { 
    if (nullptr != hose) {
      THROW_ERROR_TORT(pool_hose_wake_up (hose)); 
    }
  }

  py::object next () {
    protein pro = nullptr;
    pool_timestamp ts;
    int64 index;

    ob_retort tort = pool_next (hose, &pro, &ts, &index);
    if (POOL_NO_SUCH_PROTEIN == tort) {
      return py::object ();
    }
    if (0 > tort) {
      throw PlasmaException (tort);
    }

    return py::make_tuple (BProtein (pro), index, ts);
  }

  py::object prev() {
    protein pro = nullptr;
    pool_timestamp ts;
    int64 index;

    ob_retort tort = pool_prev (hose, &pro, &ts, &index);
    if (POOL_NO_SUCH_PROTEIN == tort) {
      return py::object ();
    }
    if (0 > tort) {
      throw PlasmaException (tort);
    }

    return py::make_tuple (BProtein (pro), index, ts);
  }

  py::object nth(int64 idx) {
    protein pro = nullptr;
    pool_timestamp ts;
    // POOL_NO_SUCH_PROTEIN is actually exceptional in this case
    THROW_ERROR_TORT (pool_nth_protein (hose, idx, &pro, &ts));
    return py::make_tuple (BProtein (pro), idx, ts);
  }

  py::object probeForward (const Slaw& s) {
    protein pro = nullptr;
    pool_timestamp ts;
    int64 idx;
    if (OB_OK == pool_probe_frwd (hose, s . peek (),
                                  &pro, &ts, &idx)) {
      return py::make_tuple (BProtein (pro), idx, ts);
    } else {
      return py::object ();
    }
  }

  py::object probeForwardAwait (const Slaw& s, const pool_timestamp timeout) {
    protein pro = nullptr;
    pool_timestamp ts;
    int64 idx;
    if (OB_OK == pool_await_probe_frwd (hose, s . peek (),
                                        timeout,
                                        &pro, &ts, &idx)) {
      return py::make_tuple (BProtein (pro), idx, ts);
    } else {
      return py::object ();
    }
  }

  py::object probeBack (const Slaw& s) {
    protein pro = nullptr;
    pool_timestamp ts;
    int64 idx;
    if (OB_OK == pool_probe_back (hose, s . peek (),
                                  &pro, &ts, &idx)) {
      return py::make_tuple (BProtein (pro), idx, ts);
    } else {
      return py::object ();
    }
  }

  py::object awaitNext(pool_timestamp timeout) {
    protein pro = nullptr;
    pool_timestamp ts;
    int64 index;

    ob_retort tort = pool_await_next (hose, timeout, &pro, &ts, &index);
    if (POOL_AWAIT_TIMEDOUT == tort || POOL_AWAIT_WOKEN == tort) {
      return py::object();
    }
    if (0 > tort) {
      throw PlasmaException (tort);
    }
 
    return py::make_tuple (BProtein (pro), index, ts);
  }
  py::object awaitNextForever() { return awaitNext (POOL_WAIT_FOREVER); }

  int64 deposit(const Slaw& pro) {
    if (! pro . isProtein ()) {
      throw PlasmaException (SLAW_CORRUPT_PROTEIN);
    }
    int64 idx;
    THROW_ERROR_TORT(pool_deposit (hose, pro . peek (), &idx));
    return idx;
  }
};

class Gang {
 private:
  pool_gang gang;

 public:
  Gang ()  :  gang (nullptr) {
    THROW_ERROR_TORT (pool_new_gang (&gang));    
  }

  ~Gang () {
    if (nullptr != gang) {
      THROW_ERROR_TORT (pool_disband_gang (gang, false));
    }
  }

  void join (const Hose& hose) {
    THROW_ERROR_TORT (pool_join_gang (gang, hose.peek ()));
  }

  void leave (const Hose& hose) {
    THROW_ERROR_TORT (pool_leave_gang (gang, hose.peek ()));
  }

  int64 count () {
    return pool_gang_count (gang);
  }

  void wakeup() {
    THROW_ERROR_TORT (pool_gang_wake_up (gang));
  }

  py::object nthHose (const int64 idx) {
    pool_hose hose = pool_gang_nth (gang, idx);
    if (nullptr != hose) {
      return py::object (pool_name (hose));
    } else {
      return py::object ();
    }
  }

  py::object awaitNext(pool_timestamp timeout) {
    pool_hose ph;
    protein pro;
    pool_timestamp ts;
    int64 idx;

    ob_retort tort = pool_await_next_multi (gang, timeout,
                                            &ph, &pro, &ts, &idx);
    if (OB_OK == tort) {
      return py::make_tuple(BProtein (pro), idx, ts, pool_name (ph));
    } else {
      if (POOL_AWAIT_TIMEDOUT == tort) {
        return py::object ();
      }
      throw PlasmaException (tort);
    }
  }

  py::object awaitNextForever() { return awaitNext (POOL_WAIT_FOREVER); }
  py::object next() { return awaitNext (0.0); }
};


//TODO: Should probably consider raising a plasma exception if there is an issue with
// the import here make PlasmaException a child of Exception using:
// class PlasmaException : virtual boost::exception, virtual std::exception
boost::python::object exceptions = boost::python::import("cplasma.exceptions");
py::dict exception_dict = py::extract<py::dict>(exceptions.attr("PLASMA_RETORT_EXCEPTIONS"));
void translatePlasmaException (PlasmaException const& e)
{ 
  const int64 retort = e.retort();
  py::object my_exception_boost;
  if (exception_dict.has_key(retort)){
      my_exception_boost = (py::object) exception_dict.get(retort);
  } else {
      my_exception_boost = py::extract<py::object>(exceptions.attr("PlasmaException"));
  }
  //Set a generic error message, this can change in the future though
  PyObject *myexc = (PyObject*) my_exception_boost.ptr();
  PyObject *myexc_inst = PyObject_CallFunction(myexc, (char *)"s", "Error");
  PyErr_SetObject(myexc, myexc_inst);
}


BOOST_PYTHON_MODULE(native)
{
  py::register_exception_translator<PlasmaException>
      (&translatePlasmaException);

  py::class_<BSlaw>
      bslawClass ("BSlaw", py::no_init);

  bslawClass
      .def ("listCount", &BSlaw::listCount, "How many items are in this list?")
      .def ("nth", &BSlaw::nth, "Get the nth item/cons in this list/map.")
      .def ("emit", &BSlaw::emit, "Transform this slaw into a Python data structure.")
      .def ("gapsearch", &BSlaw::gapsearch, "Run the gapsearch algorithm against a given slaw.")
      .def ("listFind", &BSlaw::listFind, "What is the index of the argument slaw?")
      .def ("mapFind", &BSlaw::mapFind, "Find the slaw (or nil) associated with this map key.")
      .def ("descrips", &BSlaw::descrips, "If the slaw is a protein, return its descrips. PlasmaException otherwise.")
      .def ("ingests", &BSlaw::ingests, "If the slaw is a protein, return its ingests. PlasmaException otherwise.")
      .def ("isProtein", &BSlaw::isProtein, "Is this bslaw a protein?")
      .def ("toYaml", &BSlaw::toYaml, "Dump this slaw to a yaml string")
      ;

  py::class_<BProtein>
      bproClass ("BProtein", py::no_init);

  bproClass
      .add_property("ingests", &BProtein::ingests)
      .add_property("descrips", &BProtein::descrips)
      .def("emit", &BProtein::emit)
      .def ("toYaml", &BProtein::toYaml, "Dump this protein to a yaml string")
      ;

  py::class_<Hose>
      hoseClass ("Hose", py::init<std::string> ());

  hoseClass
      .def (py::init<std::wstring> ())
      .add_property("newestIndex", &Hose::newestIndex)
      .add_property("oldestIndex", &Hose::oldestIndex)
      .add_property("index", &Hose::index)
      .add_property("name", &Hose::name)
      .def ("hoseName", &Hose::hoseName)
      .def ("setHoseName", &Hose::setHoseName)
      .def ("getInfo", &Hose::getInfo)
      .def ("enableWakeup", &Hose::enableWakeup)
      
      .def ("rewind", &Hose::rewind)
      .def ("tolast", &Hose::tolast)
      .def ("runout", &Hose::runout)
      .def ("frwdby", &Hose::frwdby)
      .def ("backby", &Hose::backby)
      .def ("seekto", &Hose::seekto)

      .def ("nth", &Hose::nth)
      .def ("next", &Hose::next)
      .def ("prev", &Hose::prev)
      .def ("awaitNext", &Hose::awaitNext)
      .def ("awaitNext", &Hose::awaitNextForever)
      .def ("probeForward", &Hose::probeForward)
      .def ("probeForwardAwait", &Hose::probeForwardAwait)
      .def ("probeBack", &Hose::probeBack)

      .def ("wakeup", &Hose::wakeup)
      .def ("deposit", &Hose::deposit)

      .def ("create", &Hose::create) . staticmethod ("create")
      .def ("dispose", &Hose::dispose) . staticmethod ("dispose")
      .def ("rename", &Hose::rename) . staticmethod ("rename")
      .def ("exists", &Hose::exists) . staticmethod ("exists")
      .def ("validateName", &Hose::validateName) . staticmethod ("validateName")
      .def ("sleep", &Hose::sleep) . staticmethod ("sleep")
      .def ("checkInUse", &Hose::checkInUse) . staticmethod ("checkInUse")
      .def ("listPools", &Hose::listPools) . staticmethod ("listPools")
      .def ("listPoolsEx", &Hose::listPools) . staticmethod ("listPoolsEx")
      ;

  py::class_<Gang>
      gangClass ("Gang");

  gangClass
      .def ("join", &Gang::join)
      .def ("leave", &Gang::leave)
      .def ("count", &Gang::count)
      .def ("awaitNext", &Gang::awaitNext)
      .def ("awaitNext", &Gang::awaitNextForever)
      .def ("next", &Gang::next)
      .def ("nthHose", &Gang::nthHose)
      .def ("wakeup", &Gang::wakeup)
      ;

  py::class_<Slaw, boost::shared_ptr<Slaw> >
      slawClass ("Slaw");

  slawClass
      .def ("read", &Slaw::read)
      .def ("make", &Slaw::from_string)
      .def ("make", &Slaw::from_stringW)
      .def ("make", &Slaw::fromBslaw)
      .def ("make", &Slaw::fromBprotein)
      DECLARE_INTS(DECLARE_SLAW_FROM,)
      DECLARE_FLOATS(DECLARE_SLAW_FROM,)
      DECLARE_INTS(DECLARE_SLAW_FROMV, v2)
      DECLARE_FLOATS(DECLARE_SLAW_FROMV, v2)
      DECLARE_INTS(DECLARE_SLAW_FROMV, v3)
      DECLARE_FLOATS(DECLARE_SLAW_FROMV, v3)
      DECLARE_INTS(DECLARE_SLAW_FROMV, v4)
      DECLARE_FLOATS(DECLARE_SLAW_FROMV, v4)
      .def ("make", &Slaw::from_numpy)
      .def ("makeArray", &Slaw::from_numpy)
      .def ("nil", &Slaw::nil)
      .def ("makeProtein", &Slaw::makeProtein)
      .def ("makeCons", &Slaw::makeCons)
      .def ("fromFile", &Slaw::fromFile)
      .def ("fromFileBinary", &Slaw::fromFileBinary)
      .def ("toYaml", &Slaw::toYaml, "Dump this slaw to a yaml string")
      .def ("fromYaml", &Slaw::fromYaml, "Create a new slaw from a yaml string")
      .def ("fromYaml", &Slaw::fromYamlW, "Create a new slaw from a yaml string")
      .def ("descrips", &Slaw::descrips, "If the slaw is a protein, return its descrips. PlasmaException otherwise.")
      .def ("ingests", &Slaw::ingests, "If the slaw is a protein, return its ingests. PlasmaException otherwise.")
      .def ("isProtein", &Slaw::isProtein, "Is this bslaw a protein?")
      .staticmethod ("make")
      .staticmethod ("makeArray")
      .staticmethod ("nil")
      .staticmethod ("makeProtein")
      .staticmethod ("fromFile")
      .staticmethod ("fromFileBinary")
      .staticmethod ("fromYaml")
      ;

  py::class_<SlawBuilder, SlawBuilder::Ref>
      slabuClass ("SlawBuilder");

  slabuClass
      .def ("takeList", &SlawBuilder::takeList)
      .def ("takeMap", &SlawBuilder::takeMap)
      .def ("listAppend", &SlawBuilder::listAppend)
      .def ("mapPut", &SlawBuilder::mapPut)
      ;

  import_array (); // <- If you don't call this, numpy functions will segfault
  py::numeric::array::set_module_and_type("numpy", "ndarray");

  REGISTER_VECT_CONVERTER(unt8, 2, NPY_UINT8);
  REGISTER_VECT_CONVERTER(int8, 2, NPY_INT8);
  REGISTER_VECT_CONVERTER(unt16, 2, NPY_UINT16);
  REGISTER_VECT_CONVERTER(int16, 2, NPY_INT16);
  REGISTER_VECT_CONVERTER(unt32, 2, NPY_UINT32);
  REGISTER_VECT_CONVERTER(int32, 2, NPY_INT32);
  REGISTER_VECT_CONVERTER(unt64, 2, NPY_UINT64);
  REGISTER_VECT_CONVERTER(int64, 2, NPY_INT64);
  REGISTER_VECT_CONVERTER(float32, 2, NPY_FLOAT32);
  REGISTER_VECT_CONVERTER(float64, 2, NPY_FLOAT64);
  
  REGISTER_VECT_CONVERTER(unt8, 3, NPY_UINT8);
  REGISTER_VECT_CONVERTER(int8, 3, NPY_INT8);
  REGISTER_VECT_CONVERTER(unt16, 3, NPY_UINT16);
  REGISTER_VECT_CONVERTER(int16, 3, NPY_INT16);
  REGISTER_VECT_CONVERTER(unt32, 3, NPY_UINT32);
  REGISTER_VECT_CONVERTER(int32, 3, NPY_INT32);
  REGISTER_VECT_CONVERTER(unt64, 3, NPY_UINT64);
  REGISTER_VECT_CONVERTER(int64, 3, NPY_INT64);
  REGISTER_VECT_CONVERTER(float32, 3, NPY_FLOAT32);
  REGISTER_VECT_CONVERTER(float64, 3, NPY_FLOAT64);
  
  REGISTER_VECT_CONVERTER(unt8, 4, NPY_UINT8);
  REGISTER_VECT_CONVERTER(int8, 4, NPY_INT8);
  REGISTER_VECT_CONVERTER(unt16, 4, NPY_UINT16);
  REGISTER_VECT_CONVERTER(int16, 4, NPY_INT16);
  REGISTER_VECT_CONVERTER(unt32, 4, NPY_UINT32);
  REGISTER_VECT_CONVERTER(int32, 4, NPY_INT32);
  REGISTER_VECT_CONVERTER(unt64, 4, NPY_UINT64);
  REGISTER_VECT_CONVERTER(int64, 4, NPY_INT64);
  REGISTER_VECT_CONVERTER(float32, 4, NPY_FLOAT32);
  REGISTER_VECT_CONVERTER(float64, 4, NPY_FLOAT64);
}
