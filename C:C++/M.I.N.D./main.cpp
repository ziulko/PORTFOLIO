#include "ComputationModule.hpp"
#include "MonteCarloPi.hpp"
#include <iostream>
#include <vector>
#include <memory>
#include <fstream>
#include <string>

size_t get_total_memory_mb() {
#ifdef __linux__
    std::ifstream meminfo("/proc/meminfo");
    std::string label;
    size_t mem_kb = 0;
    while (meminfo >> label) {
        if (label == "MemTotal:") {
            meminfo >> mem_kb;
            break;
        } else {
            std::string dummy;
            std::getline(meminfo, dummy);
        }
    }
    return mem_kb / 1024;
#else
    return 2048;
#endif
}

int main() {
    std::vector<std::unique_ptr<ComputationModule>> modules;
    modules.emplace_back(std::make_unique<MonteCarloPi>());

    size_t total_ram = get_total_memory_mb();
    size_t allowed_ram = total_ram * 60 / 100;
    std::cout << "Całkowita pamięć RAM: " << total_ram << " MB\n";
    std::cout << "Maksymalna zalecana pamięć: " << allowed_ram << " MB (60%)\n\n";

    std::cout << "Wybierz moduł obliczeniowy:\n";
    for (size_t i = 0; i < modules.size(); ++i) {
        std::cout << "[" << i + 1 << "] " << modules[i]->name() << "\n";
    }

    int choice;
    std::cout << "\nTwój wybór: ";
    std::cin >> choice;

    if (choice < 1 || choice > modules.size()) {
        std::cerr << "Nieprawidłowy wybór." << std::endl;
        return 1;
    }

    size_t limit;
    std::cout << "\nPodaj limit pamięci (MB), który może zostać użyty: ";
    std::cin >> limit;

    if (limit > allowed_ram) {
        std::cerr << "Zbyt duży limit pamięci! (rekomendowane max: " << allowed_ram << " MB)" << std::endl;
        return 1;
    }

    int precision;
    std::cout << "\nIle miejsc po przecinku obliczyć wartość π? ";
    std::cin >> precision;

    int timeout;
    std::cout << "\nUstaw maksymalny czas trwania pojedynczego obliczenia (sekundy): ";
    std::cin >> timeout;

    char use_seed;
    std::cout << "\nCzy chcesz użyć stałego ziarna RNG (y/n)? ";
    std::cin >> use_seed;

    bool fixed_seed = (use_seed == 'y' || use_seed == 'Y');
    modules[choice - 1]->run(limit, precision, timeout, fixed_seed);

    return 0;
}