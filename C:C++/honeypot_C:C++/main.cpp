#include "honeypot.hpp"
#include <iostream>
#include <sstream>
#include <csignal>

Honeypot* global_honeypot = nullptr;

void signal_handler(int signal) {
    if (global_honeypot) {
        global_honeypot->stop();
    }
    std::_Exit(0);
}

int main() {
    std::cout << "=== Modular Honeypot (C++) ===" << std::endl;
    std::cout << "Enter ports to listen on (comma-separated), or press Enter for default: ";

    std::string input;
    std::getline(std::cin, input);

    std::vector<int> ports = {80, 443};
    if (!input.empty()) {
        ports.clear();
        std::stringstream ss(input);
        std::string token;
        while (std::getline(ss, token, ',')) {
            try {
                ports.push_back(std::stoi(token));
            } catch (...) {
                std::cerr << "[ERROR] Invalid port: " << token << std::endl;
            }
        }
    }

    Honeypot honeypot(ports);
    global_honeypot = &honeypot;

    std::signal(SIGINT, signal_handler);
    std::signal(SIGTERM, signal_handler);

    honeypot.run();

    return 0;
}
