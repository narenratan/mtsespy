cmake_minimum_required(VERSION 3.10)
project(mtsespy VERSION 1.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(libs/pybind11 pybind11)

pybind11_add_module(${PROJECT_NAME})

target_sources(${PROJECT_NAME} PRIVATE
    src/mtsespy.cpp
    libs/MTS-ESP/Client/libMTSClient.cpp
    libs/MTS-ESP/Master/libMTSMaster.cpp
)

target_include_directories(${PROJECT_NAME} PUBLIC libs/MTS-ESP/Client libs/MTS-ESP/Master)

target_link_libraries(${PROJECT_NAME} PUBLIC dl)
