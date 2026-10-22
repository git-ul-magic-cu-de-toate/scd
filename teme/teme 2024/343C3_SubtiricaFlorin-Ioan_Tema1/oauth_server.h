#pragma once

#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <fstream>
#include <cstdlib>
#include <algorithm>
#include <sstream>
#include <iostream>
#include <time.h>

#include "oauth.h"
#include "helper.h"

#define TOKEN_LEN 15

class OAuthServer {
    public:
        static OAuthServer& getInstance() {
            static OAuthServer instance;
            return instance;
        }

        void initServer(int argc, char *argv[]) {
            if (argc != 5) {
                std::cerr << "./server <clients file> <resources file> <approvals file> <tokens valability>" << std::endl;
                exit(EXIT_FAILURE);
            }

            // read lines from files
            auto readLines = [](const std::string &filename, std::vector<std::string> &out) {
                std::ifstream file(filename);
                if (!file) {
                    std::cerr << "Error opening file " << filename << ".\n";
                    return false;
                }

                std::string line;
                while (getline(file, line)) {
                    out.push_back(line);
                }

                return true;
            };

            // read clients and resources
            std::vector<std::string> cli, res;

            // check if files are valid
            if (!readLines(argv[1], cli) || !readLines(argv[2], res)) {
                exit(EXIT_FAILURE);
            }

            // add clients to database
            for (size_t i = 0; i < cli.size(); i++) {
                database[cli[i]] = User();
            }

            // add resources to set
            resources.insert(res.begin() + 1, res.end());
            ttl = std::atoi(argv[4]); // token lifetime 
            responses_file.open(argv[3]); // open approvals file
        }

        std::string getAuthToken(const std::string &user_id) {
            // log request
            std::cout << "BEGIN " << user_id << " AUTHZ\n";
            std::flush(std::cout);

            // verify if user exists
            if (database.find(user_id) == database.end())
                return Operation::USER_NOT_FOUND;

            // generate auth token
            auto auth_token = std::string(generate_access_token((char* )user_id.c_str()));
            std::cout << "  RequestToken = " << auth_token << std::endl;
            std::flush(std::cout);

            // save token in database
            database[user_id].auth_token = auth_token;

            return auth_token;
        }

        struct TokenResponse {
            std::string access_token;
            std::string refresh_token;
            int ttl;
        };

        TokenResponse getAccessToken(
            const std::string &user_id,
            const std::string &request_token,
            bool refresh
        ) {
            // verify if user exists and token is valid
            auto it = database.find(user_id);
            if (it == database.end() || it->second.auth_token != request_token || it->second.permissions.empty()) {
                return {Operation::REQUEST_DENIED, Operation::EMPTY, 0};
            }

            // generate new tokens
            std::string access_token = std::string(generate_access_token((char* )request_token.c_str()));
            std::string refresh_token = refresh ?
                                        std::string(generate_access_token((char* )access_token.c_str()))
                                        : Operation::EMPTY;

            // Log new tokens
            std::cout << "  AccessToken = " << access_token << std::endl;
            if (refresh) {
                std::cout << "  RefreshToken = " << refresh_token << std::endl;
            }
            std::flush(std::cout);

            // Save data in database
            it->second = {request_token, access_token, ttl, it->second.permissions};

            return {access_token, refresh_token, ttl};
        }

        TokenResponse refreshAccessToken(
            const std::string& access_token,
            const std::string& refresh_token
        ) {
            for (auto& user : database) {
                // find user by token
                if (user.second.access_token != access_token) continue;

                // log refresh
                std::cout << "BEGIN " << user.first << " AUTHZ REFRESH\n";
                std::flush(std::cout);

                // generate new tokens
                std::string new_access_token = std::string(generate_access_token((char* )refresh_token.c_str()));
                std::string new_refresh_token = std::string(generate_access_token((char* )new_access_token.c_str()));

                // log new tokens
                std::cout << "  AccessToken = " << new_access_token << std::endl;
                std::cout << "  RefreshToken = " << new_refresh_token << std::endl;

                // update tokens in database
                user.second = {Operation::EMPTY, new_access_token, ttl, user.second.permissions};

                // return new tokens
                return {new_access_token, new_refresh_token, ttl};
            }

            // return empty tokens if user not found
            return {Operation::EMPTY, Operation::EMPTY, 0};
        }

        std::string validateAction(
            const std::string& op,
            const std::string& resource,
            const std::string& access_token
        ) {
            // search user by token
            auto user_iter = std::find_if(
                database.begin(),
                database.end(),
                [&](const auto& user) {
                    return user.second.access_token == access_token;
                }
            );

            // user not found or token is invalid
            if (access_token == Operation::EMPTY || user_iter->second.access_token != access_token) {
                printMessage(Operation::DENY, op, resource, access_token, 0);
                return Operation::PERMISSION_DENIED;
            }

            // token expired
            if (user_iter->second.ttl <= 0) {
                printMessage(Operation::DENY, op, resource, Operation::EMPTY, user_iter->second.ttl);
                return Operation::TOKEN_EXPIRED;
            }

            // decrement token lifetime
            user_iter->second.ttl--;

            // check if resource is available
            auto resource_available = std::find(resources.begin(), resources.end(), resource) != resources.end();
            if (!resource_available) {
                printMessage(Operation::DENY, op, resource, access_token, user_iter->second.ttl);
                return Operation::RESOURCE_NOT_FOUND;
            }

            // check if user has permission
            bool has_permission = std::find_if(
                user_iter->second.permissions.begin(),
                user_iter->second.permissions.end(),
                [&](const auto& perm) {
                    return perm.first == resource && perm.second.find(Operation::strToPerm(op)) != std::string::npos;
                }
            ) != user_iter->second.permissions.end();

            // permission denied
            if (!has_permission) {
                printMessage(Operation::DENY, op, resource, access_token, user_iter->second.ttl);
                return Operation::OPERATION_NOT_PERMITTED;
            }

            // permission granted
            printMessage(Operation::PERMIT, op, resource, access_token, user_iter->second.ttl);
            return Operation::PERMISSION_GRANTED;
        }

        void approveRequestToken(
            const std::string& user_id,
            const std::string& request_token
        ) {
            std::string response;
            responses_file >> response;

            // clear permissions
            database[user_id].permissions.clear();

            // check if user exists and token is valid
            if (database.find(user_id) == database.end() || database[user_id].auth_token != request_token) {
                return;
            }

            std::istringstream ss(response);
            std::string token;

            // parse response
            while (std::getline(ss, token, ',')) {
                std::string resource = token;
                if (resource == Operation::NO_APPR) {
                    // skip the wildcard resource
                    std::getline(ss, token, ',');
                    continue;
                }

                // add permissions
                if (std::getline(ss, token, ',')) {
                    std::string action = token;
                    database[user_id].permissions.push_back({resource, action});
                }
            }
        }

    private:
        struct User {
            std::string auth_token;
            std::string access_token;
            // std::string refresh_token;
            int ttl;
            std::vector<std::pair<std::string, std::string>> permissions;
        };

        OAuthServer() { }

        /**
         * generate alpha-numeric string based on random char*
         * 
         * INPUT: fixed length of 16
         * OUTPUT: rotated string
         * */
        char* generate_access_token(char* clientIdToken) {
            char *token = (char *) malloc(TOKEN_LEN * sizeof(char*));
            int i, key, used[TOKEN_LEN];
            int rotationIndex = TOKEN_LEN;

            memset(used, 0, TOKEN_LEN * sizeof(int));
            for (i = 0; i < TOKEN_LEN; i++) {
                do {
                    key = rand() % rotationIndex;
                } while (used[key] == 1);
                token[i] = clientIdToken[key];
                used[key] = 1;
            }
            token[TOKEN_LEN] = '\0';
            return token;
        }

        /**
         * print message to stdout
         */
        inline void printMessage(
            const std::string& type,
            const std::string& op,
            const std::string& resource,
            const std::string& access_token,
            int ttl
        ) {
            std::cout << type << " ("
                    << op << ","
                    << resource << ","
                    << access_token << ","
                    << ttl
                    << ")\n";

            std::flush(std::cout);
        }

    protected:
        std::unordered_set<std::string> resources;
        std::unordered_map<std::string, User> database;
        std::ifstream responses_file;
        int ttl;
};