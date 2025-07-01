# M.I.N.D – Modular Intelligence for Numeric Domains

## Project Description

**M.I.N.D** is a modular C++ framework for solving mathematical and computational problems using intelligent, resource-aware algorithms. The framework supports dynamic memory limits and concurrency controls, making it ideal for benchmarking and exploring numerical techniques on modern systems.

Each module is designed to be self-contained and share a common interface, allowing easy integration of new problem solvers such as Monte Carlo simulations, prime number searches, and future modules in algebra, integration, or optimization.

> ⚠ **Note:** M.I.N.D is under active development. While it already includes two working modules (π approximation and prime search), it is not production-ready and still undergoing refinement.

---

##  Current Features

* **Modular architecture** (based on abstract `ComputationModule`)
* **Monte Carlo π Estimator**

    * Multi-threaded random sampling
    * Optional fixed-seed comparison mode
    * Timeout-based precision progression
* **Prime Number Finder**

    * Multi-threaded Sieve of Eratosthenes
    * Execution time limit and output mode (last 10 or full)
* **Memory-aware execution**

    * Dynamic RAM limit per module (percentage of system RAM)
* **Interactive CLI interface**

    * Choose modules, configure options, set precision
* **Cross-platform support**

    * Linux (uses `/proc/meminfo`)
    * macOS (uses sysctl)
    * Fallback estimates for unsupported systems

---

## Planned Features

* Numerical integrators (e.g., trapezoidal, Simpson’s rule)
* Solver for equation roots (e.g., Newton-Raphson)
* Matrix operations module (multiplication, Gaussian elimination)
* Resource profile visualizer
* Stats summary (time, memory, precision, thread usage)

---

## Project Structure

```
src/
├── main.cpp                # CLI interface and execution logic
├── ComputationModule.hpp  # Abstract base interface for all modules
├── MonteCarloPi.hpp       # π estimation implementation
├── PrimeFinder.hpp        # Prime number finder module
└── utils/                  # Memory detection, helper functions (planned)
```

---

## Technologies Used

* **C++17**
* `std::thread`, `std::chrono`, `std::atomic` – for concurrency and timing
* Conditional compilation for system-specific RAM usage detection
* Clean separation of modules and core engine logic

---

## Example Run (Monte Carlo Module)

```
Select computation module:
[1] Monte Carlo π Estimator
[2] Prime Number Finder

Memory Limit (MB): 1200
Precision (decimal places): 10
Timeout per step (seconds): 60
Use fixed seed (y/n)? n

[1 decimal places] Estimated Pi = 3.1
[2 decimal places] Estimated Pi = 3.14
...
```

---

## Status

**WIP** – M.I.N.D is a learning and demonstration project with plans to grow into a full-featured, modular numerical computing suite. Additional modules, accuracy metrics, and performance dashboards are in development.

---

## Contributions & Ideas

Feel free to open issues or suggest new computational modules. This project is ideal for experimentation, learning multithreading, or exploring system-aware performance strategies.
