/* used as params for request_auth_token */
struct request_start_auth {
    string user_id<>;
};

/* used as result for request_auth_token */
struct response_get_auth_token {
    string auth_token<>;
    bool is_error;
    string message<>;
};

/* used as params for approve_auth_token */
struct start_approve_auth {
    string auth_token<>;
};

/* used as result for approve_auth_token */
struct response_approve_auth {
    bool is_signed;
    string auth_token<>;
};

/* used as params for request_bearer_token */
struct request_bearer_token_args {
    bool is_signed;
    bool automatic_refresh;
    string auth_token<>;
    string user_id<>;
};

/* used as result for request_bearer_token */
struct response_start_auth {
    int token_lifetime;
    bool is_error;
    string message<>;
    string access_token<>;
    string refresh_token<>;
};

/* used as args for validate_delegated_action */
struct request_validate_action {
    string operation<>;
    string resource<>;
    string access_token<>;
};

/* used as result for validate_delegated_action */
struct response_validate_action {
    string message<>;
    string access_token<>;
};

/* used as args for renew_bearer_token */
struct request_renew_bearer_token {
    string access_token<>;
};

/* used as args for renew_bearer_token */
struct response_renew_bearer_token {
    bool is_error;
    string access_token<>;
};

program OAUTH_PROG {
    version OAUTH_VERS {
        /* generate an auth_token for an user_id */
        response_get_auth_token REQUEST_AUTH_TOKEN(request_start_auth) = 1;
        /* approve an auth_token by getting permissions on resources */
        response_approve_auth APPROVE_AUTH_TOKEN(start_approve_auth) = 2;
        /* generate an access_token (and refresh_token) for an auth_token signed */
        response_start_auth REQUEST_BEARER_TOKEN(request_bearer_token_args) = 3;
        /* start an action on a resource and checks if the user that has the acces token
             can do the action */
        response_validate_action VALIDATE_DELEGATED_ACTION(request_validate_action) = 4;
        /* for an user with automatic refresh enabled regenerate an access_token and refresh_token
            by using the refresh_token assigned to the access_token provided to the request */
        response_renew_bearer_token RENEW_BEARER_TOKEN(request_renew_bearer_token) = 5;
    } = 1;
} = 1;