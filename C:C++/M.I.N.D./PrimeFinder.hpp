#pragma once
#include "ComputationModule.hpp"
#include <thread>
#include <atomic>
#include <vector>
#include <iostream>
#include <cmath>
#include <chrono>

class PrimeFinder : public ComputationModule {
public:
    std::string name() const override {
        return "Prime Number Finder";
    }

    void run(size_t memory_limit_mb, int max_number = 1000000, int timeout_seconds = 60, bool = false, bool full_output = false) override {
        std::atomic<bool> done(false);
        auto start_time = std::chrono::steady_clock::now();

        std::vector<bool> is_prime(max_number + 1, true);
        is_prime[0] = is_prime[1] = false;

        int thread_count = std::thread::hardware_concurrency();
        if (thread_count == 0) thread_count = 2;

        auto sieve_worker = [&](int tid) {
            for (int i = 2 + tid; i * i <= max_number; i += thread_count) {
                if (is_prime[i]) {
                    for (int j = i * i; j <= max_number; j += i) {
                        is_prime[j] = false;
                    }
                }
                auto now = std::chrono::steady_clock::now();
                if (std::chrono::duration_cast<std::chrono::seconds>(now - start_time).count() > timeout_seconds) {
                    done = true;
                    return;
                }
            }
        };

        std::vector<std::thread> threads;
        for (int i = 0; i < thread_count; ++i) {
            threads.emplace_back(sieve_worker, i);
        }
        for (auto& t : threads) t.join();

        std::vector<int> primes;
        for (int i = 2; i <= max_number && !done; ++i) {
            if (is_prime[i]) primes.push_back(i);
        }

        std::cout << "\nZnaleziono " << primes.size() << " liczb pierwszych <= " << max_number << ".\n";
        if (full_output) {
            for (size_t i = 0; i < primes.size(); ++i) {
                std::cout << primes[i] << " ";
                if ((i + 1) % 20 == 0) std::cout << "\n";
            }
        } else {
            std::cout << "Ostatnie 10: ";
            for (int i = std::max(0, (int)primes.size() - 10); i < primes.size(); ++i) {
                std::cout << primes[i] << " ";
            }
        }
        std::cout << "\n";
    }
};