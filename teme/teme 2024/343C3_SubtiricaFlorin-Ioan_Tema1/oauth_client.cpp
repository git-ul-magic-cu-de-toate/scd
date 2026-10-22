#include <iostream>
#include <fstream>
#include <iterator>
#include <string>
#include <unordered_map>
#include <vector>
#include <rpc/rpc.h>
#include <rpc/xdr.h>

#include "oauth.h"
#include "helper.h"

struct Client {
    std::string auth_token;
    std::string access_token;
    std::string refresh_token;
    int ttl;
};

std::unordered_map<std::string, Client> database;
CLIENT *clnt;

// Function to split a string by a delimiter
std::vector<std::string> split(const std::string& str, char delimiter) {
    std::vector<std::string> tokens;
    size_t start = 0, end;
    while ((end = str.find(delimiter, start)) != std::string::npos) {
        tokens.push_back(str.substr(start, end - start));
        start = end + 1;
    }
    tokens.push_back(str.substr(start)); // Add the last token
    return tokens;
}

void requestAccessToken(const std::string& userID, bool refresh) {
    // Request for authorization token
    AuthRequest auth_request{const_cast<char*>(userID.c_str())};
    auto auth_response = requestauthorization_1(auth_request, clnt);
    if (!auth_response || std::string(auth_response->request_token) == Operation::USER_NOT_FOUND) {
        std::cout << Operation::USER_NOT_FOUND << std::endl;
        return;
    }

    std::string request_token = auth_response->request_token;

    // Approve request token
    ApproveRequestToken approve_request{const_cast<char*>(userID.c_str()), const_cast<char*>(request_token.c_str())};
    approverequest_1(approve_request, clnt);

    // Request for access token
    AccessTokenRequest access_token_request{const_cast<char*>(userID.c_str()), const_cast<char*>(request_token.c_str()), refresh};
    auto token_data = requestaccesstoken_1(access_token_request, clnt);
    if (!token_data || std::string(token_data->access_token) == Operation::REQUEST_DENIED) {
        std::cout << Operation::REQUEST_DENIED << std::endl;
        return;
    }

    // Log the access token and refresh token
    std::cout << request_token << " -> " << token_data->access_token
              << (refresh ? "," + std::string(token_data->refresh_token) : "") << std::endl;

    // Save the token data in the database
    database[userID] = Client{
        request_token, token_data->access_token, token_data->refresh_token, token_data->ttl
    };
}

void validateAction(const std::string& userID, const std::string& op, const std::string& resource) {
    auto& user = database[userID];

    // Verify if token is expired and refresh token is available
    if (user.ttl <= 0 && !user.refresh_token.empty()) {
        RefreshTokenRequest refresh_token_request{
            const_cast<char*>(user.access_token.c_str()), const_cast<char*>(user.refresh_token.c_str())
        };
        auto tokenData = refreshaccesstoken_1(refresh_token_request, clnt);
        if (!tokenData) {
            std::cout << Operation::TOKEN_EXPIRED << std::endl;
            return;
        }

        database[userID] = Client{
            user.auth_token, tokenData->access_token, tokenData->refresh_token, tokenData->ttl
        };
    }

    // Send the request to the server to validate the action
    ValidateActionRequest validate_action_request{
        const_cast<char*>(op.c_str()), const_cast<char*>(resource.c_str()), const_cast<char*>(user.access_token.c_str())
    };
    auto response = validateaction_1(validate_action_request, clnt);
    if (!response) {
        std::cout << Operation::ERR << std::endl;
        return;
    }

    // Decrease the token lifetime if the action was successful
    --user.ttl;
    
    std::cout << response->response << std::endl;
}

void doAction(const std::string& action) {
    // Split the action string by comma
    const auto fields = split(action, ',');
    if (fields.size() < 3) {
        std::cerr << "Invalid action format" << std::endl;
        return;
    }

    // Check if the action is a request for access token else validate the action
    if (fields[1] == "REQUEST") {
        requestAccessToken(static_cast<std::string>(fields[0]), fields[2] == "1");
    } else {
        validateAction(fields[0], fields[1], fields[2]);
    }
}

int main(int argc, char* argv[]) {
    clnt = clnt_create(argv[1], OAUTH_PROG, OAUTH_VERS, "tcp");

    if (clnt == nullptr) {
        clnt_pcreateerror(argv[1]);
        exit(EXIT_FAILURE);
    }

    // Read the actions from the file
    std::ifstream file(argv[2]);
    std::string line;
    // iterate through each line of the file and perform the action
    while (std::getline(file, line)) {
        doAction(line);
    }

    clnt_destroy(clnt);
    return 0;
}
