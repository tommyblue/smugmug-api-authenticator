from rauth import OAuth1Service, OAuth1Session

OAUTH_BASE = "https://secure.smugmug.com"
REQUEST_TOKEN_URL = OAUTH_BASE + "/services/oauth/1.0a/getRequestToken"
ACCESS_TOKEN_URL = OAUTH_BASE + "/services/oauth/1.0a/getAccessToken"
AUTHORIZE_URL = OAUTH_BASE + "/services/oauth/1.0a/authorize"
API_BASE = "https://api.smugmug.com"

SERVICE = None


def setup_service(key=None, secret=None):
    global SERVICE
    if SERVICE is None:
        SERVICE = OAuth1Service(
            name="smugmug-oauth-web-demo",
            consumer_key=key,
            consumer_secret=secret,
            request_token_url=REQUEST_TOKEN_URL,
            access_token_url=ACCESS_TOKEN_URL,
            authorize_url=AUTHORIZE_URL,
            base_url=API_BASE + "/api/v2",
        )


def get_user_session(app_key, app_secret, user_token, user_secret):
    return OAuth1Session(
        app_key, app_secret, access_token=user_token, access_token_secret=user_secret,
    )


def setup_auth(cb_url):
    req_token, req_secret = SERVICE.get_request_token(params={"oauth_callback": cb_url})
    return req_token, req_secret


def verify_callback(oauth_verifier: str, req_token: str, req_secret: str):
    user_token, user_secret = SERVICE.get_access_token(
        req_token, req_secret, params={"oauth_verifier": oauth_verifier},
    )

    return user_token, user_secret
