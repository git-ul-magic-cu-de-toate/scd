#ifndef CLIENT_H_
#define CLIENT_H_

#include <iostream>
#include <string>
#include <pthread.h>
#include <fstream>
#include <utility>
#include <unordered_map>
#include <vector>

#define TOKEN_LEN 15

struct LoggedClient {
    bool automatic_refresh;
    std::string user_id;
    std::string access_token;
};

#endif  // CLIENT_H_