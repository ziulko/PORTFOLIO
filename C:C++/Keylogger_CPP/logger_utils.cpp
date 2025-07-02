#include "logger_utils.h"
#include <filesystem>
#include <chrono>
#include <iomanip>
#include <sstream>
#include <fstream>

#if defined(__APPLE__)
#include <mach-o/dyld.h>
#elif defined(__linux__)
#include <unistd.h>
#include <limits.h>
#endif

namespace fs = std::filesystem;

std::ofstream logfile;

void create_log_file() {
    fs::path base_dir;

#if defined(__APPLE__)
    char path_buf[PATH_MAX];
    uint32_t buf_size = sizeof(path_buf);
    if (_NSGetExecutablePath(path_buf, &buf_size) == 0) {
        fs::path full_path(path_buf);
        base_dir = full_path.parent_path().parent_path();
    } else {
        base_dir = fs::current_path();
    }
#elif defined(__linux__)
    char exe_path[PATH_MAX];
    ssize_t count = readlink("/proc/self/exe", exe_path, PATH_MAX);
    if (count != -1) {
        fs::path full_path(exe_path);
        base_dir = full_path.parent_path().parent_path();
    } else {
        base_dir = fs::current_path();
    }
#else
    base_dir = fs::current_path();
#endif

    base_dir /= "logs";
    fs::create_directories(base_dir);

    auto now = std::chrono::system_clock::now();
    std::time_t t_now = std::chrono::system_clock::to_time_t(now);
    std::tm local_tm = *std::localtime(&t_now);

    std::ostringstream date_stream;
    date_stream << std::put_time(&local_tm, "%Y-%m-%d");
    std::string date_str = date_stream.str();

    fs::path daily_dir = base_dir / date_str;
    fs::create_directory(daily_dir);

    int session_id = 1;
    fs::path session_file;
    do {
        session_file = daily_dir / ("session_" + std::to_string(session_id) + ".txt");
        session_id++;
    } while (fs::exists(session_file));

    logfile.open(session_file);
}
