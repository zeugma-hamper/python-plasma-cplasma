
// see http://www.boost.org/doc/libs/1_55_0/libs/python/doc/v2/numeric.html

#include <signal.h>

#include <libPlasma/c/pool.h>
#include <libPlasma/c/protein.h>
#include <libPlasma/c/slaw.h>

#include <boost/python.hpp>
#include <boost/python/numeric.hpp>
#include <numpy/ndarrayobject.h>

#include <string>
#include <list>

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

#define RETURN_IF_NUMERIC(TYP, s) do {          \
    if (slaw_is_ ## TYP (s)) {                  \
      const TYP *tmp;                           \
      tmp = slaw_ ## TYP ## _emit (s);          \
      return py::object (*tmp);                 \
    }                                           \
  } while (false)

#define RETURN_IF_NUMERIC2(TYP, s) do {                 \
    if (slaw_is_v2 ## TYP (s)) {                        \
      const v2 ## TYP *tmp;                             \
          tmp = slaw_v2 ## TYP ## _emit (s);            \
              return py::numeric::array(tmp -> x,       \
                                        tmp -> y);      \
    }                                                   \
  } while (false)


#define RETURN_IF_NUMERIC3(TYP, s) do {                         \
    if (slaw_is_v3 ## TYP (s)) {                                        \
      auto tmp = slaw_v3 ## TYP ## _emit (s);                           \
          double data [3];                                              \
          data[0] = tmp -> x;                                           \
          data[1] = tmp -> y;                                           \
          data[2] = tmp -> z;                                           \
          double* dp = &data[0];                                        \
          npy_intp size = 3;                                            \
          PyObject* pyObj = PyArray_SimpleNewFromData (1, &size, NPY_DOUBLE, dp); \
          boost::python::handle<> handle (pyObj);                       \
          boost::python::numeric::array arr (handle);                   \
          return arr.copy ();                                           \
    }                                                                   \
  } while (false)

#define RETURN_IF_NUMERIC4(TYP, s) do {         \
    if (slaw_is_ ## TYP (s)) {                  \
      const TYP *tmp;                           \
      tmp = slaw_ ## TYP ## _emit (s);          \
          return py::numeric::array(tmp -> x,   \
                                    tmp -> y,   \
                                    tmp -> z,   \
                                    tmp -> w);  \
    }                                           \
  } while (false)


#define FOR_ALL_INTS(M, PRE, s)                 \
  M (PRE ## unt8, s);                           \
  M (PRE ## int8, s);                           \
  M (PRE ## unt16, s);                          \
  M (PRE ## int16, s);                          \
  M (PRE ## unt32, s);                          \
  M (PRE ## unt64, s);                          \
  M (PRE ## int64, s);

#define FOR_ALL_FLOATS(M, PRE, s)               \
  M (PRE ## float32, s);                        \
  M (PRE ## float64, s);

class BSlaw {
 private:
  bslaw slaw_;

 public:
  BSlaw (bslaw s) : slaw_ { s } {}

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

  py::object emit_numeric_vector_array () const { return py::object(); }
  py::object emit_numeric_vector () const {
    // FOR_ALL_INTS(RETURN_IF_NUMERIC2, , slaw_);
    FOR_ALL_INTS(RETURN_IF_NUMERIC3, , slaw_);
    // FOR_ALL_INTS(RETURN_IF_NUMERIC4, , slaw_);
    // FOR_ALL_FLOATS(RETURN_IF_NUMERIC2, , slaw_);
    FOR_ALL_FLOATS(RETURN_IF_NUMERIC3, , slaw_);
    // FOR_ALL_FLOATS(RETURN_IF_NUMERIC4, , slaw_);
    return py::object();
  }
  py::object emit_numeric_array () const { return py::object(); }
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

  unt64 list_count () const {
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
    tort = pool_hose_enable_wakeup (hose);
    if (0 > tort) {
      pool_withdraw (hose);
      hose = nullptr;
      throw PlasmaException (tort);
    }
  }

  virtual ~Hose () {
    if (nullptr != hose) {
      pool_withdraw (hose);
    }
  }

  const char* name() const {
    return pool_name (hose);
  }

  int64 newest_index() const {
    int64 out;
    THROW_ERROR_TORT(pool_newest_index(hose, &out));
    return out;
  }

  int64 oldest_index() const {
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

  py::object await_next(pool_timestamp timeout) {
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

    // py::list ret;
    
    // ret.append (BProtein (pro));
    // ret.append (index);
    // ret.append (ts);
    // return ret;
  }

  py::object await_next_forever() { return await_next (POOL_WAIT_FOREVER); }
};



static PyObject *plasmaExceptionType = nullptr;
void translatePlasmaException (PlasmaException const& e)
{ assert (nullptr != plasmaExceptionType);
  py::object pythonExceptionInstance (e);
  PyErr_SetObject(plasmaExceptionType, pythonExceptionInstance.ptr());
}

void fail() {
  throw PlasmaException (OB_NOT_FOUND);
}


BOOST_PYTHON_MODULE(cplasma)
{ py::class_<PlasmaException>
      plasmaExceptionClass ("PlasmaException",
                            py::init<ob_retort> ());
  plasmaExceptionClass
      .add_property("description", &PlasmaException::description)
      .add_property("retort", &PlasmaException::retort);
  plasmaExceptionType = plasmaExceptionClass . ptr ();
  py::register_exception_translator<PlasmaException>
      (&translatePlasmaException);

  py::class_<BSlaw>
      bslawClass ("BSlaw", py::no_init);

  bslawClass
      .add_property ("list_count", &BSlaw::list_count)
      .def ("emit", &BSlaw::emit)
      ;

  py::class_<BProtein>
      bproClass ("BProtein", py::no_init);

  bproClass
      .add_property("ingests", &BProtein::ingests)
      .add_property("descrips", &BProtein::descrips)
      ;

  py::class_<Hose>
      hoseClass ("Hose", py::init<std::string> ());

  hoseClass
      .add_property("newest_index", &Hose::newest_index)
      .add_property("oldest_index", &Hose::oldest_index)
      .add_property("index", &Hose::index)
      .add_property("name", &Hose::name)

      .def ("rewind", &Hose::rewind)
      .def ("tolast", &Hose::tolast)
      .def ("runout", &Hose::runout)
      .def ("frwdby", &Hose::frwdby)
      .def ("backby", &Hose::backby)
      .def ("seekto", &Hose::seekto)
      
      .def ("await_next", &Hose::await_next)
      .def ("await_next", &Hose::await_next_forever)

      .def ("wakeup", &Hose::wakeup)
      ;

  py::numeric::array::set_module_and_type("numpy", "ndarray");
}
