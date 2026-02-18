# Robotics Arm Control (3-DOF): Algorithmic IK vs ML IK

This repository implements a complete assignment scaffold for comparing:

1. Traditional analytical inverse kinematics in C++
2. Neural-network-based inverse kinematics in Python + C++ ONNX Runtime inference

## Project Layout

```text
.
├── CMakeLists.txt
├── include/
│   ├── CollisionChecker.h
│   ├── Controller.h
│   ├── IKSolver.h
│   ├── MLIKSolver.h
│   ├── RobotArm.h
│   └── TrajectoryPlanner.h
├── src/
│   ├── CollisionChecker.cpp
│   ├── Controller.cpp
│   ├── IKSolver.cpp
│   ├── MLIKSolver.cpp
│   ├── RobotArm.cpp
│   ├── TrajectoryPlanner.cpp
│   └── main.cpp
├── tests/
│   └── test_kinematics.cpp
└── ml/
    ├── benchmark_report.py
    ├── dataset_generator.py
    ├── requirements.txt
    ├── train_model.py
    └── visualize_arm.py
```

## Implemented Features

- 3-DOF arm model with FK and joint-position reconstruction
- Analytical IK with multiple configurations (elbow-up/down)
- Joint limit validation (`[-pi, pi]`)
- Cubic time-scaled joint interpolation
- Sphere-obstacle collision checking with link sampling
- End-to-end controller loop with position error feedback
- Optional ONNX Runtime C++ inference module
- Python dataset generation (`50k+`) and model training
- ONNX export with explicit input/output names for C++ integration
- Basic test executable for FK/IK consistency

## Build and Run (Algorithmic)

### Linux / macOS

```bash
mkdir -p build
cd build
cmake ..
cmake --build . -j
./robot_control
./test_kinematics
```

### Windows (PowerShell)

```powershell
mkdir build
cd build
cmake ..
cmake --build . --config Release
.\Release\robot_control.exe
.\Release\test_kinematics.exe
```

`robot_control` writes trajectory files such as `trajectory_0.txt`.

## ML Dataset and Training

Install dependencies:

```bash
pip install -r ml/requirements.txt
```

Generate dataset:

```bash
python ml/dataset_generator.py --samples 50000 --out ml/dataset.npz
```

Train and export ONNX:

```bash
python ml/train_model.py --dataset ml/dataset.npz --out-onnx models/ik_model.onnx
```

## C++ ONNX Inference

Build with ONNX Runtime:

```bash
cmake -S . -B build -DENABLE_ONNXRUNTIME=ON -DONNXRUNTIME_DIR=/path/to/onnxruntime
cmake --build build -j
```

Run ML benchmark path:

```bash
./build/robot_control models/ik_model.onnx
```

When a model path is provided, `robot_control` prints ML inference time and Cartesian target error.

## Visualization Demo

Animate trajectory:

```bash
python ml/visualize_arm.py --traj trajectory_0.txt --target 0.28 0.10 0.22
```

## Notes for Report

Collect and compare:

- IK latency (`analytical` vs `ML`)
- End-effector error at target
- Success rate on reachable/unreachable targets
- Behavior near obstacles and workspace boundaries

For CSV summary post-processing:

```bash
python ml/benchmark_report.py --csv your_raw_runs.csv --out benchmark_summary.csv
```
# Robotics-C-Machine-learning-
