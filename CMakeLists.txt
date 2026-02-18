cmake_minimum_required(VERSION 3.16)
project(RoboticArmControl LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

option(ENABLE_ONNXRUNTIME "Build ML IK solver with ONNX Runtime" OFF)

find_package(Eigen3 3.3 REQUIRED NO_MODULE)

add_library(robot_core
    src/RobotArm.cpp
    src/IKSolver.cpp
    src/TrajectoryPlanner.cpp
    src/CollisionChecker.cpp
    src/Controller.cpp
    src/MLIKSolver.cpp
)
target_include_directories(robot_core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(robot_core PUBLIC Eigen3::Eigen)

add_executable(robot_control src/main.cpp)
target_link_libraries(robot_control PRIVATE robot_core)

add_executable(test_kinematics tests/test_kinematics.cpp)
target_link_libraries(test_kinematics PRIVATE robot_core)

add_executable(benchmark src/benchmark.cpp)
target_link_libraries(benchmark PRIVATE robot_core)

if(ENABLE_ONNXRUNTIME)
    if(NOT DEFINED ONNXRUNTIME_DIR)
        message(FATAL_ERROR "ENABLE_ONNXRUNTIME=ON requires -DONNXRUNTIME_DIR=/path/to/onnxruntime")
    endif()
    target_compile_definitions(robot_core PUBLIC USE_ONNXRUNTIME=1)
    target_include_directories(robot_core PUBLIC ${ONNXRUNTIME_DIR}/include)
    target_link_directories(robot_core PUBLIC ${ONNXRUNTIME_DIR}/lib)
    target_link_libraries(robot_core PUBLIC onnxruntime)
endif()
