#ifndef SERVER_H_
#define SERVER_H_

#include <iostream>
#include <string>
#include <pthread.h>
#include <fstream>
#include <utility>
#include <unordered_map>
#include <vector>

#define READ "READ"
#define MODIFY "MODIFY"
#define EXECUTE "EXECUTE"
#define DELETE "DELETE"
#define INSERT "INSERT"

#define USER_NOT_FOUND "USER_NOT_FOUND"
#define REQUEST_DENIED "REQUEST_DENIED"
#define EMPTY_TOKEN "EMPTY_TOKEN"
#define PERMISSION_DENIED "PERMISSION_DENIED"
#define RENEW_TOKEN "RENEW_TOKEN"
#define TOKEN_EXPIRED "TOKEN_EXPIRED"
#define RESOURCE_NOT_FOUND "RESOURCE_NOT_FOUND"
#define OPERATION_NOT_PERMITTED "OPERATION_NOT_PERMITTED"
#define PERMISSION_GRANTED "PERMISSION_GRANTED"

// users database struct
struct UserEntry {
    std::string user_id;
    std::string auth_token; // needed for adding the permissions without knowing the id
    std::string access_token;
    std::string refresh_token;
    bool automatic_refresh;
    int tokens_lifetime;
    std::unordered_map<std::string, std::vector<std::string>> permissions;
};

// server global variables used between server and oauth_svc
extern std::vector<UserEntry> users_database;
extern std::vector<std::string> resources;
extern std::vector<std::string> approvals;
extern int token_lifetime;

#endif  // SERVER_H_