# M.I.N.D – Modular Intelligence for Numeric Domains

## Project Description

**M.I.N.D** is a modular C++ framework designed for solving mathematical and computational problems using intelligent, resource-aware algorithms. Each module is designed to work within memory and concurrency constraints, enabling efficient and scalable numerical computations on modern multi-core systems.

The goal is to offer an extensible environment where multiple computational modules (such as π estimation, prime search, numerical integration) can be run independently with adjustable memory and performance parameters.

>⚠ **Note:** M.I.N.D is currently in an early development stage. Only a single module (Monte Carlo π Estimator) is implemented. More modules and resource policies are planned for future versions.

---

## Current Features

- Modular architecture (based on a shared abstract interface)
- Monte Carlo-based π approximation using multi-threading
- Runtime memory limit for each module
- Thread-aware task scheduling
- Command-line interface (CLI) with interactive module selection
- Available memory detection (Linux)
- Cross-platform build-ready structure

---

## Planned Modules

-  Prime number range search
-  Numerical integrator (e.g., trapezoidal rule)
-  Solver for equation roots or optimization
-  Matrix multiplication and linear algebra utilities

---

## Technologies Used

- C++17 (compatible with C++20)
- `std::thread`, `std::atomic`, `std::chrono` – for concurrency and timing
- Linux system file access (`/proc/meminfo`) for memory checks
- Cross-platform fallback compatibility

---

## Project Structure

```plaintext
src/
├── main.cpp                # CLI interface and execution control
├── ComputationModule.hpp  # Abstract base class for modules
├── MonteCarloPi.hpp       # Monte Carlo π Estimator implementation
└── (more modules soon...)
