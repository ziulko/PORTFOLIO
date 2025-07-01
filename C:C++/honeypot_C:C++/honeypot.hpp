#pragma once
#include <vector>
#include <string>

class Honeypot {
public:
    Honeypot(const std::vector<int>& ports);
    void run();
    void stop(); // Dodane

private:
    std::vector<int> ports;
    std::string session_id;
    std::string log_directory;
    bool running;

    void listen_on_port(int port);
    void create_log_directory();
    std::string get_timestamp() const;
    void log_event(int port, const std::string& client_ip, const std::string& data = "");
    void generate_summary() const;
};
