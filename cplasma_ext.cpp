
// (c) 2014 MCT

#include <iostream>

#include <libPlasma/c/pool.h>
#include <libPlasma/c/protein.h>
#include <libPlasma/c/slaw.h>

#include <boost/python.hpp>
#include <boost/shared_ptr.hpp>
#include <numpy/ndarrayobject.h> 

#include <string>
#include <vector>

namespace py = boost::python;

class PlasmaException : public std::exception {
 private:
  ob_retort tort;

 public:
  PlasmaException(ob_retort t)  :  tort { t } {}

  const char* description() const { return ob_error_string (tort); }
  const ob_retort retort() const { return tort; }
};

#define THROW_ERROR_TORT(expr) do {             \
    ob_retort tort = expr;                      \
    if (0 > tort) {                             \
      throw PlasmaException (tort);             \
    }                                           \
  } while (false)


#define DECLARE_INTS(M, PRE)                         \
  M(PRE##unt8)                                       \
  M(PRE##int8)                                       \
  M(PRE##unt16)                                      \
  M(PRE##int16)                                      \
  M(PRE##unt32)                                      \
  M(PRE##int32)                                      \
  M(PRE##unt64)                                      \
  M(PRE##int64)

#define DECLARE_FLOATS(M, PRE)                  \
  M(PRE##float32)                               \
  M(PRE##float64)


template <typename T> struct array_writer {};

#define FOR_ALL_INTS(M, PRE, s)                 \
  M (PRE ## unt8, s);                           \
  M (PRE ## int8, s);                           \
  M (PRE ## unt16, s);                          \
  M (PRE ## int16, s);                          \
  M (PRE ## unt32, s);                          \
  M (PRE ## int32, s);                          \
  M (PRE ## unt64, s);                          \
  M (PRE ## int64, s);

#define FOR_ALL_FLOATS(M, PRE, s)               \
  M (PRE ## float32, s);                        \
  M (PRE ## float64, s);

#define RETURN_IF_NUMERIC(TYP, s) do {          \
    if (slaw_is_ ## TYP (s)) {                  \
      const TYP *tmp;                           \
      tmp = slaw_ ## TYP ## _emit (s);          \
      return py::object (*tmp);                 \
      }                                         \
  } while (false)

#define RETURN_IF_NUMARRAY(TYP, s) do {                          \
    if (slaw_is_ ## TYP ## _array (s)) {                         \
      const TYP *tmp = slaw_ ## TYP ## _array_emit (s);          \
          const int64 N = slaw_numeric_array_count (s);          \
          py::list lst;                                          \
          for (int64 i = 0; i < N; ++i) {                        \
            lst.append(tmp[i]);                                  \
          }                                                      \
          return lst;                                            \
    }                                                            \
  } while (false)

#define RETURN_IF_V2(TYP, s) do {               \
    if (slaw_is_v2 ## TYP (s)) {                \
      auto ptr = slaw_v2 ## TYP ## _emit (s);   \
          py::list lst;                         \
          lst.append(ptr -> x);                 \
          lst.append(ptr -> y);                 \
          return lst;                           \
    }                                           \
  } while (false)

#define RETURN_IF_V3(TYP, s) do {               \
    if (slaw_is_v3 ## TYP (s)) {                \
      auto ptr = slaw_v3 ## TYP ## _emit (s);   \
          py::object ret(*ptr);                 \
          return ret;                           \
    }                                           \
  } while (false)


#define RETURN_IF_V4(TYP, s) do {               \
    if (slaw_is_v4 ## TYP (s)) {                \
      auto ptr = slaw_v4 ## TYP ## _emit (s);   \
          py::list lst;                         \
          lst.append(ptr -> x);                 \
          lst.append(ptr -> y);                 \
          lst.append(ptr -> z);                 \
          lst.append(ptr -> w);                 \
          return lst;                           \
    }                                           \
  } while (false)
      

class BSlaw {
 private:
  bslaw slaw_;

 public:
  BSlaw (bslaw s) : slaw_ { s } {}

  slaw dup () { return slaw_dup (slaw_); }

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
    py::dict dct;
    bslaw s = slaw_list_emit_first (slaw_);
    while (s != NULL) {
      BSlaw car { slaw_cons_emit_car (s) };
      BSlaw cdr { slaw_cons_emit_cdr (s) };
      dct . setdefault (car.emit(), cdr.emit());
      s = slaw_list_emit_next (slaw_, s);
    }
    return dct;
  }

  py::object emit_cons () const {
    BSlaw car { slaw_cons_emit_car (slaw_) };
    BSlaw cdr { slaw_cons_emit_cdr (slaw_) };
    return py::make_tuple (car, cdr);
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

  py::object emit () const {
    if (slaw_is_list (slaw_)) {
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

  unt64 listCount () const {
    return slaw_list_count (slaw_);
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
};

#define STR(X) #X

#define PREDECLARE_V2(T)                            \
  v2##T make_v2##T (T x, T y) {                     \
    v2##T out = { x, y };                           \
        return out;                                 \
  }                                                 \
  std::string repr_v2##T (const v2##T& v) {         \
    std::stringstream out;                          \
    out << STR(v2##T) << '('                        \
    << v.x << ',' << v.y << ')';                    \
    return out.str();                               \
  }

#define PREDECLARE_V3(T)                            \
  v3##T make_v3##T (T x, T y, T z) {                \
    v3##T out = { x, y, z };                        \
        return out;                                 \
  }                                                 \
  std::string repr_v3##T (const v3##T& v) {         \
    std::stringstream out;                          \
    out << STR(v3##T) << '('                        \
    << v.x << ','                                   \
    << v.y << ','                                   \
    << v.z << ')';                                  \
    return out.str();                               \
  }

#define PREDECLARE_V4(T)                            \
  v4##T make_v4##T (T x, T y, T z, T w) {           \
    v4##T out = { x, y, z, w };                     \
        return out;                                 \
  }                                                 \
  std::string repr_v4##T (const v4##T& v) {         \
    std::stringstream out;                          \
    out << STR(v4##T) << '('                        \
    << v.x << ','                                   \
    << v.y << ','                                   \
    << v.z << ','                                   \
    << v.w << ')';                                  \
    return out.str();                               \
  }

#define DECLARE_V2(T)                               \
  py::class_<v2##T> (STR(v2##T))                    \
  .def_readwrite("x", &v2##T::x)                    \
  .def_readwrite("y", &v2##T::y)                    \
  .def("__repr__", &repr_v2##T)                     \
  .def("make", &make_v2##T).staticmethod("make")    \
  ;

#define DECLARE_V3(T)                               \
  py::class_<v3##T> (STR(v3##T))                    \
  .def_readwrite("x", &v3##T::x)                    \
  .def_readwrite("y", &v3##T::y)                    \
  .def_readwrite("z", &v3##T::z)                    \
  .def("__repr__", &repr_v3##T)                     \
  .def("make", &make_v3##T).staticmethod("make")    \
  ;

#define DECLARE_V4(T)                               \
  py::class_<v4##T> (STR(v4##T))                    \
  .def_readwrite("x", &v4##T::x)                    \
  .def_readwrite("y", &v4##T::y)                    \
  .def_readwrite("z", &v4##T::z)                    \
  .def_readwrite("w", &v4##T::w)                    \
  .def("__repr__", &repr_v4##T)                     \
  .def("make", &make_v4##T).staticmethod("make")    \
  ;


DECLARE_INTS(PREDECLARE_V2,);
DECLARE_INTS(PREDECLARE_V3,);
DECLARE_INTS(PREDECLARE_V4,);
DECLARE_FLOATS(PREDECLARE_V2,);
DECLARE_FLOATS(PREDECLARE_V3,);
DECLARE_FLOATS(PREDECLARE_V4,);

#define SLAW_FROM_NUMERIC(T)                                    \
  static Ref from_ ## T (T t) {                                 \
    return Ref(new Slaw (slaw_##T (t)));                        \
  }

#define DECLARE_SLAW_FROM(T)                    \
  .def("make", &Slaw::from_ ##T)                \
  .def(STR(make_ ## T), &Slaw::from_ ##T)       \
  .staticmethod(STR(make_ ## T))

class Slaw {
 private:
  slaw slaw_ = nullptr;

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
  
  static Ref fromBslaw (BSlaw bs) {
    return Ref(new Slaw (bs.dup()));
  }

  static Ref fromBprotein (BProtein bp) {
    return Ref (new Slaw (bp.dup()));
  }

  static Ref from_string (std::string s) {
    return Ref(new Slaw (slaw_string (s.c_str())));
  }

  static Ref makeCons (Ref car, Ref cdr) {
    return Ref (new Slaw (slaw_cons_ff (car -> take (),
                                        cdr -> take ())));
  }
  
  DECLARE_INTS (SLAW_FROM_NUMERIC,);
  DECLARE_FLOATS (SLAW_FROM_NUMERIC,);

  DECLARE_INTS (SLAW_FROM_NUMERIC, v2);
  DECLARE_FLOATS (SLAW_FROM_NUMERIC, v2);

  DECLARE_INTS (SLAW_FROM_NUMERIC, v3);
  DECLARE_FLOATS (SLAW_FROM_NUMERIC, v3);

  DECLARE_INTS (SLAW_FROM_NUMERIC, v4);
  DECLARE_FLOATS (SLAW_FROM_NUMERIC, v4);

  static Ref nil() { return Ref (new Slaw (slaw_nil())); }
  
  static Ref from_obj(py::object &obj) {
    if (obj . is_none ()) {
      return nil();
    }

    PyObject* typ_ = PyObject_Type (obj . ptr ());
    py::handle<> h (py::borrowed (typ_));
    py::object typ (h);
    py::extract<std::string> nam (typ);
    if (nam . check ()) {
      std::cerr << "having trouble with type "
                << nam() << "\n";
    } else {
      std::cerr << "Could not coerce a type to a string\n";
    }

    throw PlasmaException (SLAW_FABRICATOR_BADNESS);
  }

#define NPYARR_SINGLE(NPYTYP, OBTYP)                            \
  if (typ == NPYTYP) {                                          \
    OBTYP* data = reinterpret_cast<OBTYP*> (buffer);            \
    return Ref(new Slaw (slaw_##OBTYP##_array(data, len)));     \
  }


#define NPYARR_DOUBLE(NPYTYP, OBTYP)                                    \
  if (typ == NPYTYP) {                                                  \
    v2##OBTYP* data = reinterpret_cast<v2##OBTYP*> (buffer);            \
        return Ref(new Slaw (slaw_v2##OBTYP##_array(data, len)));       \
  }

#define NPYARR_TRIPLE(NPYTYP, OBTYP)                                    \
  if (typ == NPYTYP) {                                                  \
    v3##OBTYP* data = reinterpret_cast<v3##OBTYP*> (buffer);            \
        return Ref(new Slaw (slaw_v3##OBTYP##_array(data, len)));       \
  }


#define NPYARR_QUAD(NPYTYP, OBTYP)                                      \
  if (typ == NPYTYP) {                                                  \
    v4##OBTYP* data = reinterpret_cast<v4##OBTYP*> (buffer);            \
        return Ref(new Slaw (slaw_v4##OBTYP##_array(data, len)));       \
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

  static Ref makeProtein (Ref des, Ref ing) {
    return Ref(new Slaw (protein_from_ff(des -> take (),
                                         ing -> take ())));
  }
};

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
 public:
  Hose (std::string pool) : hose { nullptr } {
    ob_retort tort = pool_participate (pool . c_str (),
                                       &hose,
                                       nullptr);
    if (0 > tort) {
      hose = nullptr; // belt, suspenders
      throw PlasmaException (tort);
    }
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
    return OB_OK == pool_exists (name . c_str ());
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
      THROW_ERROR_TORT (pool_disband_gang (gang, true));
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
      if (0 > tort) {
        throw PlasmaException (tort);
      }
      return py::object ();
    }
  }

  py::object awaitNextForever() { return awaitNext (POOL_WAIT_FOREVER); }
  py::object next() { return awaitNext (0.0); }
};

static PyObject *plasmaExceptionType = nullptr;
void translatePlasmaException (PlasmaException const& e)
{ assert (nullptr != plasmaExceptionType);
  py::object pythonExceptionInstance (e);
  PyErr_SetObject(plasmaExceptionType, pythonExceptionInstance.ptr());
}

BOOST_PYTHON_MODULE(native)
{ py::class_<PlasmaException>
      plasmaExceptionClass ("PlasmaException",
                            py::init<ob_retort> ());
  plasmaExceptionClass
      .add_property("description", &PlasmaException::description)
      .add_property("retort", &PlasmaException::retort);
  plasmaExceptionType = plasmaExceptionClass . ptr ();
  py::register_exception_translator<PlasmaException>
      (&translatePlasmaException);

  // Give us our nice, juicy v{2,3,4}TYPE types
  DECLARE_INTS(DECLARE_V2,);
  DECLARE_INTS(DECLARE_V3,);
  DECLARE_INTS(DECLARE_V4,);
  DECLARE_FLOATS(DECLARE_V2,);
  DECLARE_FLOATS(DECLARE_V3,);
  DECLARE_FLOATS(DECLARE_V4,);

  py::class_<BSlaw>
      bslawClass ("BSlaw", py::no_init);

  bslawClass
      .add_property ("listCount", &BSlaw::listCount)
      .def ("emit", &BSlaw::emit)
      ;

  py::class_<BProtein>
      bproClass ("BProtein", py::no_init);

  bproClass
      .add_property("ingests", &BProtein::ingests)
      .add_property("descrips", &BProtein::descrips)
      .def("emit", &BProtein::emit)
      ;

  py::class_<Hose>
      hoseClass ("Hose", py::init<std::string> ());

  hoseClass
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
      ;

  py::class_<Slaw, boost::shared_ptr<Slaw> >
      slawClass ("Slaw");

  slawClass
      .def ("make", &Slaw::from_obj)
      .def ("read", &Slaw::read)
      .def ("make", &Slaw::from_string)
      .def ("make", &Slaw::fromBslaw)
      .def ("make", &Slaw::fromBprotein)
      DECLARE_INTS(DECLARE_SLAW_FROM,)
      DECLARE_FLOATS(DECLARE_SLAW_FROM,)
      DECLARE_INTS(DECLARE_SLAW_FROM, v2)
      DECLARE_FLOATS(DECLARE_SLAW_FROM, v2)
      DECLARE_INTS(DECLARE_SLAW_FROM, v3)
      DECLARE_FLOATS(DECLARE_SLAW_FROM, v3)
      DECLARE_INTS(DECLARE_SLAW_FROM, v4)
      DECLARE_FLOATS(DECLARE_SLAW_FROM, v4)
      .def ("make", &Slaw::from_numpy)
      .def ("makeArray", &Slaw::from_numpy)
      .def ("nil", &Slaw::nil)
      .def ("makeProtein", &Slaw::makeProtein)
      .def ("makeCons", &Slaw::makeCons)
      .staticmethod ("make")
      .staticmethod ("makeArray")
      .staticmethod ("nil")
      .staticmethod ("makeProtein")
      ;

  py::class_<SlawBuilder, SlawBuilder::Ref>
      slabuClass ("SlawBuilder");

  slabuClass
      .def ("takeList", &SlawBuilder::takeList)
      .def ("takeMap", &SlawBuilder::takeMap)
      .def ("listAppend", &SlawBuilder::listAppend)
      .def ("mapPut", &SlawBuilder::mapPut)
      ;

  py::numeric::array::set_module_and_type("numpy", "ndarray");
}