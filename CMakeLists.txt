
cmake_minimum_required (VERSION 2.8.8)
project (cplasma)

if (DEFINED CMAKE_BUILD_TYPE)
   set(CMAKE_BUILD_TYPE ${CMAKE_BUILD_TYPE} CACHE STRING "Choose the type of build, options are: Debug Release")
else()
   set(CMAKE_BUILD_TYPE Debug CACHE STRING "Choose the type of build, options are: Debug Release")
endif()

include_directories (${cplasma_SOURCE_DIR})
include_directories ("/usr/include/python2.7")
include_directories ("/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/numpy/core/include")

set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

# Warning and other flags
if (${CMAKE_SYSTEM_NAME} MATCHES "Linux")
  foreach (CXX_FLAG -Wtype-limits
                    -Wno-unused-command-line-argument -Wvla)
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CXX_FLAG}")
  endforeach ()
endif ()

foreach (CXX_FLAG -Wempty-body -fdiagnostics-show-option -Wall -Wpointer-arith
                  -Wno-unused-function
                  -Wshadow -Wwrite-strings -Wno-overloaded-virtual
                  -Wno-strict-overflow -Wno-error=unused-variable -Werror
                  -g -O3 -std=c++11)
  set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CXX_FLAG}")
endforeach ()


set (CMAKE_CXX_COMPILER "clang++")
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wno-parentheses -Wno-unused-command-line-argument -Wno-shadow")

include_directories (${cplasma_SOURCE_DIR})
include_directories (${cplasma_SOURCE_DIR}/folly)

set (G_SPEAK_MIN_VERSION "3.12")
include (${cplasma_SOURCE_DIR}/bld/g-speak-sdk.cmake)
set (G_SPEAK_YOBUILD_HOME ${G_SPEAK_DEPS})

set (CMAKE_CXX_FLAGS "-I ${cplasma_SOURCE_DIR}/gtest/include ${CMAKE_CXX_FLAGS}")

enable_testing()

set (g_speak_deps "")
foreach (g_speak_dep libLoam libPlasma)
  set (g_speak_deps "${g_speak_deps} ${g_speak_dep}")
endforeach ()

execute_process (
  COMMAND ${PKG_CONFIG_EXECUTABLE} ${g_speak_deps} --cflags
  OUTPUT_VARIABLE G_SPEAK_DEFINITIONS
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

# work around bug in yovo's pkgconfig files
string (
  REGEX REPLACE " -pthread" "" G_SPEAK_DEFINITIONS "${G_SPEAK_DEFINITIONS}"
)

execute_process (
  COMMAND ${PKG_CONFIG_EXECUTABLE} ${g_speak_deps} --libs --static
  OUTPUT_VARIABLE G_SPEAK_LIBRARIES
  OUTPUT_STRIP_TRAILING_WHITESPACE
)

message(STATUS " CPLASMA_INCLUDE_DIRS is ${G_SPEAK_INCLUDE_DIRS}\n")
message(STATUS " CPLASMA_LIBRARIES is ${G_SPEAK_LIBRARIES}\n")
message(STATUS " CPLASMA_DEFINITIONS is ${G_SPEAK_DEFINITIONS}\n")
message(STATUS " CPLASMA_YOBUILD_HOME is ${G_SPEAK_YOBUILD_HOME}\n")

INCLUDE_DIRECTORIES(${G_SPEAK_INCLUDE_DIRS})
set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${G_SPEAK_DEFINITIONS}")

set(cplasma_ext_sources cplasma_ext.cpp)

add_library(cplasma_ext MODULE cplasma_ext.cpp)
target_link_libraries(cplasma_ext -lboost_python -lboost_numpy -lpython2.7 ${G_SPEAK_LIBRARIES})
set_target_properties(cplasma_ext PROPERTIES PREFIX "")

