#include <cassert>
#include <cstdio>
#include <cstdint>
#include <cinttypes>
#include <string>
#include <vector>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <liburing.h>
#include <fileio.h>
#include <utils.h>

constexpr int MAX_EVENTS = 4096;
constexpr int MIN_NR = 1;


