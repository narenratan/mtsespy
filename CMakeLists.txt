cmake_minimum_required(VERSION 3.15...3.26)

project(mtsespy VERSION "0.1.0")

# Find the module development requirements (requires FindPython from 3.17 or
# scikit-build-core's built-in backport)
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

set(python_module_name _mtsespy)
pybind11_add_module(${python_module_name} MODULE
  src/mtsespy/mtsespy.cpp
)

target_sources(_mtsespy PRIVATE
    src/mtsespy/mtsespy.cpp
    libs/MTS-ESP/Client/libMTSClient.cpp
    libs/MTS-ESP/Master/libMTSMaster.cpp
)

target_include_directories(_mtsespy PUBLIC libs/MTS-ESP/Client libs/MTS-ESP/Master libs/tuning-library/include)

install(TARGETS ${python_module_name} DESTINATION mtsespy)
