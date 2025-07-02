cmake_minimum_required(VERSION 3.10)
project(Keylogger)
set(CMAKE_CXX_STANDARD 17)

if(APPLE)
    find_library(APP_SERVICES ApplicationServices)
    add_executable(Keylogger
            main.cpp
            logger_utils.cpp
            keylogger_macos.cpp
            active_window_macos.cpp
    )
    target_link_libraries(Keylogger ${APP_SERVICES})
endif()