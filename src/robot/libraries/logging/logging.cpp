#include "logging.h"

#define LOGGING 1
#ifdef LOGGING

// logging is enabled
#include <Arduino.h>
#include <stdio.h>
#include <stdarg.h>

void logIt(char* format, ...)
{
    char line[1024];
    va_list args;
    va_start(args, format);
    vsnprintf(line, sizeof(line), format, args);
    va_end(args);
    Serial.print(line);
    Serial.print("\n");
}

#else

// logging is disabled
void logIt(char* format, ...)
{
    // no op
}

#endif
