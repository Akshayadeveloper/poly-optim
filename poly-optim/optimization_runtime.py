
import time
import functools
from typing import Callable, Any

# Threshold for optimization (in seconds)
OPTIMIZATION_THRESHOLD = 0.005 

# Dictionary to track function performance and whether it's been 'optimized'
performance_registry = {}

# --- External Compiler/Runner Mock ---
def _execute_compiled_core(args, kwargs) -> Any:
    """
    MOCK: This represents the call to the compiled (C/Rust) or highly-optimized 
    intermediate representation (IR) runner. It's assumed to be much faster.
    """
    print("\n[POLYOPTIM] Executing compiled, optimized kernel...")
    # Mocking the actual optimized calculation (e.g., matrix operations in C)
    result = sum(args[0]) * 2 + kwargs.get('offset', 0)
    time.sleep(0.0001) # Very fast execution time
    return result

def poly_optimize(target_func: Callable):
    """
    Decorator that intelligently decides whether to run the native function 
    or the highly-optimized compiled kernel based on runtime profiling.
    """
    func_name = target_func.__name__
    performance_registry[func_name] = {"optimized": False, "total_runs": 0, "avg_time": 0}

    @functools.wraps(target_func)
    def wrapper(*args, **kwargs):
        global performance_registry
        stats = performance_registry[func_name]

        if stats["optimized"]:
            return _execute_compiled_core(args, kwargs)

        # Start Profiling
        start_time = time.perf_counter()
        result = target_func(*args, **kwargs)
        end_time = time.perf_counter()
        
        execution_time = end_time - start_time
        stats["total_runs"] += 1
        
        # Update running average time
        if stats["total_runs"] == 1:
            stats["avg_time"] = execution_time
        else:
            stats["avg_time"] = (stats["avg_time"] * (stats["total_runs"] - 1) + execution_time) / stats["total_runs"]

        # Optimization Check
        if stats["avg_time"] > OPTIMIZATION_THRESHOLD and not stats["optimized"]:
            print(f"\n[POLYOPTIM] --- Threshold crossed. Activating optimization for {func_name} ---")
            stats["optimized"] = True # Flip the switch for future runs
            
        print(f"[Profiling] Run time: {execution_time*1000:.2f}ms | Avg Time: {stats['avg_time']*1000:.2f}ms")
        return result

    return wrapper

# --- Demonstration: A function that simulates heavy computation ---

@poly_optimize
def heavy_data_process(data: List[int], offset: int = 100):
    """Native Python implementation (slow)."""
    print(f"[Native] Running heavy process for {len(data)} items...")
    # Simulate a time-consuming calculation
    result = 0
    for x in data:
        result += x * 2
        time.sleep(0.0005) # Simulate latency
    return result + offset

# Initial calls are slow and trigger the optimization
data_set = [i for i in range(10)]
print("--- Run 1 (Native) ---")
heavy_data_process(data_set, offset=10)

print("\n--- Run 2 (Native) ---")
heavy_data_process(data_set, offset=20)

# Subsequent calls are automatically redirected to the mock optimized kernel
print("\n--- Run 3 (Optimized Kernel) ---")
heavy_data_process(data_set, offset=30)
  
