341C3 - Mihai Daniel Soare
Software Systems for Computer Networks

Homework 1 - OAUTH using RPC framework in C++

November 2023

-------------

How to use the program
----------------------

__Commands__

- use the `make build` command in `src` directory to build the `server` and `client` binaries
- use the ./check.sh all to check all the tests

__Tasks Done__

- i have implemented all the tasks requested in the task sheet of the homework

__Changes Made__

- i have changed the tests files: `server.out` and `client.out` by adding a `\n`
in all the files cause there was a discrepancy between my output and the tests output

*  ouath.x
    - this is the interface of the application
    - has 5 methods available available between the client and server:
        - request_auth_token
        - approve_auth_token
        - request_bearer_token
        - validate_delegated_action
        - renew_bearer_token
    - for each method available there are 2 structs used:
        - request: meant to be the args for the request
        - response: meant to be the result of the request

* ouath_svc.cpp
    - this is the part of the server that does the reading of the files provided by user
    - if there weren't provided enough files there will be an error

* server.cpp
    - has the implementation of each method of the application's interface
    - has a list of users (users_database)
    - has a list of approvals provided by 3rd party apps
    - has a list of resources available

* client.cpp
    - does the reading of the clients requests
    - start to run the requests in a sequential order
    - can do 2 requests: start_authentication and start_action_on_resource
    - has a list of clients authenticated at the moment

__Structs__

A. `request_auth_token`

- request_auth_token
    - user_id - used for searching the user in the users database

- response_get_auth_token
    - auth_token - gets as a response if the user was added in the database
    - is_error - gets an error if the user wasn't added
    - message - gets a message of the output

B. `approve_auth_token`

- start_approve_auth
    - auth_token - used for signing the token and getting a list of permissions

- response_approve_auth
    - is_signed - signs the auth_token
    - returns the auth_token

C. `request_bearer_token`

- request_bearer_token_args
    - auth_token - used for generating a bearer token = (acc token, refresh token)
    - user_id - used for searching in the database where to add the bearer token
    - is_signed - used for checking the previous approve request
    - automatic_refresh - used to generate a refresh token if it is enabled

- response_start_auth
    - access_token - the access token generated
    - refresh_token - the refresh token generated
    - is_error - used for checking if the auth_token was signed and if the tokens
    can be generated
    - message

D. `validate_delegated_action`

- request_validate_action
    - operation
    - resource
    - access_token - needed to know which user is doing the request

- response_validate_action
    - access_token - returns a new access token if the automatic refresh is on, otherwise
    returns the old access_token
    - message - returns a message of how the running of the action went

E. `renew_bearer_token`

- request_renew_bearer_token
    - access_token - used for identifying the user in the database and getting the refresh_token
    straight from the users_database

- response_renew_bearer_token
    - is_error
    - access_token - returns a new access_token used for identifying the user after
    refreshing the tokens

Server
------

- implements the 5 methods from the interface

- there are global variables defined to be used between the `server` and `server_svc` files

__Requests__

A. `request_auth_token`

- generate an auth_token for users that were added in the users_database

B. `approve_auth_token`

- for an auth_token provided by the client, gets a line of permissions for resources
from the `approvals` file

- if there weren't any available permissions, the request will return an `is_signed=false`

- otherwise, an `is_signed=true`

(!!!!)
- i decided to add the permissions in the users database in this method, to me it seemed the
best moment to do it cause won't have to return them to the client anymore

C. `request_bearer_token`

- check if the auth_token provided as argument was signed `is_signed=true`

- returns the error if the auth_token wasn't signed

- generate an access_token from the auth_token provided

- generate a refresh_token if the automatic refresh provided is enabled

- adds in the database the access_token, refresh_token, tokens_lifetime and if the automatic
refresh is enabled

D. `validate_delegated_action`

- for an access_token provided by the client check if it is empty aka has value `EMPTY_TOKEN`,
have decided to use this cause of a problem that appeared when checking if the access_token
is null

- checks if by any chance there is a discrepancy between the user and client database
of active users, and returns permission_denied when the access_token doesn't exist
in the users_database

- checks if the access_token provided by the client has expired (has the token_lifetime equal to 0)
and if the user has automatic refresh enabled

- if the user has automatic refresh enabled, send a `RENEW_TOKEN` to the client and the client
will renew the bearer_token and will retry validating the same action on the same resource

- if the user doesn't have automatic refrash enabled, then token expired

- otherwise, continue to check if the resource is available and the user has permissions to start
an action on that resource

- at the end of this request, the result should be permission_granted cause it passed all the checks

E. `renew_bearer_token`

- for an access_token provided by the client, checks if the user exist in the database and gets
the refresh_token assigned to that user

- generate a new access_token and a new refresh_token by using the old refresh_token of the user

- update the new tokens and the lifetime

- also returns to the client the updated access_token

Client
------

- the client has a list of logged clients

- the logged clients are a struct containing: user_id, access_token and automatic_refresh

(!!!)
- to me there was no point in storing the refresh_token, with only access_token available the client
can make a request to the server and the server has in the database an association between the:
access_token and the refresh_token, so the user will only be providing access_token after it was generated

- has 2 methods available:
    -> start_authentication
    -> start_action_on_resource

__Requests__

A. `start_authentication`

- use `request_auth_token` to get an auth_token

- use `approve_request_token` to approve if there are permissions available for this request

- use `request_bearer_token` to get an access_token and a refresh_token (if automatic refresh is enabled)

- update the client in the `clients_authenticated` list stored on the client

B. `start_action_on_resource`

- gets the access_token for each client authenticated

- start validating the action by running a `validate_delegated_action` with args:
access_token, operation and resource

- if the user doesn't have automatic refresh enabled and the token has expired, the client needs to
removed from the list of clients authenticated

- if the user has automatic refresh enabled, the response will be `RENEW_TOKEN` so the client can use `renew_bear_token` to generate a new one

- then try again to `validate_delegated_action`

- print the final response from the server

(!!!)
- i have decided to not use the refresh_token directly in the client, but in the server

- the client will provide the access_token and the server will get the assigned refresh_token