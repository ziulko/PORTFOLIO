#include "active_window_utils.h"
#include <ApplicationServices/ApplicationServices.h>
#include <string>

std::string get_active_app_name() {
    CFArrayRef windowList = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID);
    std::string appName = "Unknown";

    for (CFIndex i = 0; i < CFArrayGetCount(windowList); i++) {
        CFDictionaryRef dict = (CFDictionaryRef)CFArrayGetValueAtIndex(windowList, i);
        CFStringRef ownerName = (CFStringRef)CFDictionaryGetValue(dict, kCGWindowOwnerName);
        if (ownerName) {
            char buffer[256];
            if (CFStringGetCString(ownerName, buffer, sizeof(buffer), kCFStringEncodingUTF8)) {
                appName = buffer;
                break;
            }
        }
    }

    CFRelease(windowList);
    return appName;
}