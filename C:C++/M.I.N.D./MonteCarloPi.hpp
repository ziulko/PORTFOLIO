#pragma once
#include "ComputationModule.hpp"
#include <atomic>
#include <thread>
#include <vector>
#include <random>
#include <chrono>
#include <iostream>
#include <iomanip>
#include <cmath>

class MonteCarloPi : public ComputationModule {
public:
    std::string name() const override {
        return "Monte Carlo π Estimator";
    }

    void run(size_t memory_limit_mb, int decimal_precision = 5, int timeout_seconds = 60, bool fixed_seed = false) override {
        std::atomic<long long> inside_circle(0);
        std::atomic<long long> total_points(0);
        int threads_count = std::thread::hardware_concurrency();
        if (threads_count == 0) threads_count = 2;

        auto overall_start = std::chrono::high_resolution_clock::now();

        double target_precision = std::pow(10, -decimal_precision);
        double pi_estimate = 0.0;
        int current_precision = 1;
        bool timeout_triggered = false;

        while (current_precision <= decimal_precision && !timeout_triggered) {
            std::atomic<bool> done(false);
            inside_circle = 0;
            total_points = 0;
            auto start = std::chrono::high_resolution_clock::now();

            auto worker = [&](unsigned int seed) {
                std::mt19937 rng(fixed_seed ? std::mt19937(seed) : std::mt19937(std::random_device{}()));
                std::uniform_real_distribution<double> dist(0.0, 1.0);
                long long local_inside = 0;
                long long local_total = 0;
                while (!done.load()) {
                    double x = dist(rng);
                    double y = dist(rng);
                    if (x * x + y * y <= 1.0) ++local_inside;
                    ++local_total;

                    if (local_total % 100000 == 0) {
                        double current_pi = 4.0 * (double)(inside_circle + local_inside) / (total_points + local_total);
                        if (std::fabs(current_pi - M_PI) < std::pow(10, -current_precision)) {
                            done = true;
                            break;
                        }
                    }
                }
                inside_circle += local_inside;
                total_points += local_total;
            };

            std::vector<std::thread> threads;
            for (int i = 0; i < threads_count; ++i) {
                threads.emplace_back(worker, i + 1);
            }

            std::thread timer_thread([&]() {
                auto timeout_start = std::chrono::steady_clock::now();
                while (!done.load()) {
                    auto now = std::chrono::steady_clock::now();
                    auto elapsed = std::chrono::duration_cast<std::chrono::seconds>(now - timeout_start).count();
                    if (elapsed >= timeout_seconds) {
                        timeout_triggered = true;
                        done = true;
                        break;
                    }
                    std::this_thread::sleep_for(std::chrono::milliseconds(100));
                }
            });

            for (auto& t : threads) t.join();
            timer_thread.join();

            auto end = std::chrono::high_resolution_clock::now();
            std::chrono::duration<double> duration = end - start;

            pi_estimate = 4.0 * static_cast<double>(inside_circle.load()) / total_points;
            std::cout << std::fixed << std::setprecision(current_precision);
            std::cout << "\n[" << current_precision << " decimal places] Estimated Pi = " << pi_estimate;
            std::cout << " in " << duration.count() << " seconds";
            if (timeout_triggered) {
                std::cout << " (timeout).";
            }
            std::cout << std::endl;

            ++current_precision;
        }

        auto overall_end = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> total_duration = overall_end - overall_start;
        std::cout << "\nFinal Pi Estimate: " << std::setprecision(decimal_precision) << pi_estimate;
        std::cout << "\nTotal Time Elapsed: " << total_duration.count() << " seconds.\n";
    }
};