#include "honeypot.hpp"
#include <iostream>
#include <fstream>
#include <thread>
#include <mutex>
#include <chrono>
#include <ctime>
#include <sstream>
#include <iomanip>
#include <netinet/in.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <filesystem>

#define BUFFER_SIZE 1024

std::mutex log_mutex;

Honeypot::Honeypot(const std::vector<int>& ports) : ports(ports), running(true) {
    session_id = get_timestamp();
    create_log_directory();
    std::cout << "[DEBUG] Logs saved to: " << log_directory << std::endl;
}

void Honeypot::run() {
    std::vector<std::thread> threads;
    for (int port : ports) {
        threads.emplace_back(&Honeypot::listen_on_port, this, port);
    }
    for (auto& t : threads) {
        t.join();
    }
    generate_summary();
}

void Honeypot::stop() {
    running = false;
    std::cout << "\n[INFO] Gracefully shutting down...\n";
    generate_summary();
}

void Honeypot::listen_on_port(int port) {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int opt = 1;
    socklen_t addrlen = sizeof(address);

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket failed");
        return;
    }

    setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR, &opt, sizeof(opt));

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(port);

    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        close(server_fd);
        return;
    }

    if (listen(server_fd, 5) < 0) {
        perror("Listen failed");
        close(server_fd);
        return;
    }

    std::cout << "[INFO] Listening on port " << port << std::endl;

    while (running) {
        new_socket = accept(server_fd, (struct sockaddr*)&address, &addrlen);
        if (new_socket < 0) {
            if (running) perror("Accept failed");
            continue;
        }

        char client_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &address.sin_addr, client_ip, INET_ADDRSTRLEN);

        std::cout << "[RECEIVED] Connection from " << client_ip << " on port " << port << std::endl;
        log_event(port, client_ip);

        send(new_socket, "Welcome to secure service\n", 26, 0);

        char buffer[BUFFER_SIZE] = {0};
        int valread = read(new_socket, buffer, BUFFER_SIZE);
        if (valread > 0) {
            std::cout << "[DATA] " << client_ip << ": " << buffer << std::endl;
            log_event(port, client_ip, std::string(buffer));
        }

        close(new_socket);
    }

    close(server_fd);
}

void Honeypot::create_log_directory() {
    std::filesystem::path logBase = std::filesystem::current_path();
    if (logBase.filename() == "cmake-build-debug" || logBase.filename() == "build") {
        logBase = logBase.parent_path();
    }

    log_directory = logBase / "honeypot_logs" / ("session_" + session_id);
    std::filesystem::create_directories(log_directory);
}


std::string Honeypot::get_timestamp() const {
    auto now = std::chrono::system_clock::now();
    std::time_t now_time = std::chrono::system_clock::to_time_t(now);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&now_time), "%Y-%m-%d_%H-%M-%S");
    return ss.str();
}

void Honeypot::log_event(int port, const std::string& client_ip, const std::string& data) {
    std::lock_guard<std::mutex> lock(log_mutex);
    std::string filename = log_directory + "/port_" + std::to_string(port) + ".log";
    std::ofstream log_file(filename, std::ios::app);
    if (log_file.is_open()) {
        std::string ts = get_timestamp();
        log_file << "[" << ts << "] " << client_ip;
        if (!data.empty()) {
            log_file << " | Data: " << data;
        }
        log_file << "\n";
    }
}

void Honeypot::generate_summary() const {
    std::string summary_file = log_directory + "/summary.txt";
    std::ofstream out(summary_file);
    if (out.is_open()) {
        out << "Honeypot session summary for session " << session_id << "\n";
        out << "Ports monitored: ";
        for (int port : ports) {
            out << port << " ";
        }
        out << "\nSession logs saved in: " << log_directory << "\n";
    }
}
