#include "logger.hpp"
#include <fstream>
#include <iostream>
#include <sstream>
#include <mutex>
#include <ctime>
#include <map>
#include <vector>
#include <set>

namespace {
    std::mutex log_mutex;
    std::string session_id;
    std::map<int, std::vector<std::string>> session_logs;
    std::set<std::string> unique_ips;

    std::string get_timestamp() {
        std::time_t now = std::time(nullptr);
        char buf[100];
        std::strftime(buf, sizeof(buf), "%Y-%m-%d_%H-%M-%S", std::localtime(&now));
        return std::string(buf);
    }
}

void Logger::init_session() {
    session_id = get_timestamp();
    std::cout << "Starting honeypot session ID: " << session_id << "\n";
}

void Logger::log_event(int port, const std::string& ip, const std::string& data) {

    std::lock_guard<std::mutex> lock(log_mutex);
    std::ostringstream entry;
    entry << "[" << get_timestamp() << "] Connection from " << ip;
    if (!data.empty()) {
        entry << " | Data: " << data;
    }

    session_logs[port].push_back(entry.str());
    unique_ips.insert(ip);
    std::cout << "[DEBUG] Logging event for port " << port << " from " << "\n";
}

void Logger::finalize_report() {
    std::ofstream summary("honeypot_summary_" + session_id + ".log");
    summary << "Session Summary (" << session_id << ")\n\n";

    for (const auto& [port, entries] : session_logs) {
        summary << "Port " << port << " (" << entries.size() << " connections):\n";
        for (const auto& e : entries) {
            summary << e << "\n";
        }
        summary << "\n";
    }

    summary << "Unique IPs: " << unique_ips.size() << "\n";
    for (const auto& ip : unique_ips) {
        summary << " - " << ip << "\n";
    }

    std::cout << "[INFO] Session summary written to file.\n";
}