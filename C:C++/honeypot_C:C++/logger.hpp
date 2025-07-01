#pragma once
#include <string>

namespace Logger {
    void init_session();
    void log_event(int port, const std::string& ip, const std::string& data = "");
    void finalize_report();
}