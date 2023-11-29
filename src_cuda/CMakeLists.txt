cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(AI LANGUAGES CXX CUDA)

set(CUDA_TOOLKIT_ROOT_DIR "/nix/store/i42cbmdf8l1xr6y3z310k6d4dc3gyrrh-cudatoolkit-11.7.0")
set(CMAKE_PREFIX_PATH "${CUDA_TOOLKIT_ROOT_DIR};${CMAKE_PREFIX_PATH}")

set(CMAKE_CUDA_ARCHITECTURES 75)
include_directories(${CMAKE_SOURCE_DIR})

set(PROJECT_SOURCES main.cc)

# Create the executable
add_executable(${PROJECT_NAME} ${PROJECT_SOURCES})

set_target_properties(${PROJECT_NAME} PROPERTIES
                      CXX_STANDARD 17
                      CXX_STANDARD_REQUIRED YES
                      CUDA_STANDARD 17
                      CUDA_STANDARD_REQUIRED YES)

# Link libraries (if any)
# target_link_libraries(${PROJECT_NAME} <library_name>)
