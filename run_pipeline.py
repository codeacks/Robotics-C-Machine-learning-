import subprocess
import os
import sys

def run_command(cmd, shell=False):
    print(f"Executing: {cmd}")
    subprocess.check_call(cmd, shell=shell)

def main():
    # 1. Dataset Generation
    run_command([sys.executable, "ml/dataset_generator.py", "--samples", "50000"])

    # 2. Training
    run_command([sys.executable, "ml/train_model.py", "--epochs", "50"])

    # 3. Build C++ (Optional, if user has build tools)
    print("Please ensure C++ code is built with -DENABLE_ONNXRUNTIME=ON and -DONNXRUNTIME_DIR=...")
    
    # 4. If build/benchmark exists, run it
    benchmark_exe = "build/benchmark" if os.name != 'nt' else "build/Release/benchmark.exe"
    if os.path.exists(benchmark_exe):
        run_command([benchmark_exe, "models/ik_model.onnx", "1000"])
        
        # 5. Summary Report
        if os.path.exists("benchmark_results.csv"):
            run_command([sys.executable, "ml/benchmark_report.py", "--csv", "benchmark_results.csv"])
    else:
        print(f"Skipping benchmark run. {benchmark_exe} not found.")

if __name__ == "__main__":
    main()
