#pragma once
#include <string>

class ComputationModule {
public:
    virtual std::string name() const = 0;
    virtual void run(size_t memory_limit_mb, int param = 5, int timeout_seconds = 60, bool fixed_seed = false, bool full_output = false) = 0;
    virtual ~ComputationModule() = default;
};