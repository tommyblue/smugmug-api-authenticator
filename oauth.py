from rauth import OAuth1Service, OAuth1Session

OAUTH_BASE = "https://secure.smugmug.com"
REQUEST_TOKEN_URL = OAUTH_BASE + "/services/oauth/1.0a/getRequestToken"
ACCESS_TOKEN_URL = OAUTH_BASE + "/services/oauth/1.0a/getAccessToken"
AUTHORIZE_URL = OAUTH_BASE + "/services/oauth/1.0a/authorize"
API_BASE = "https://api.smugmug.com"

APP_KEY = None
APP_SECRET = None
SERVICE = None

REQ_TOKEN = None
REQ_SECRET = None

USER_TOKEN = None
USER_SECRET = None


def setup_service(key=None, secret=None):
    global APP_KEY
    global APP_SECRET
    global SERVICE
    if SERVICE is None:
        APP_KEY = key
        APP_SECRET = secret
        SERVICE = OAuth1Service(
            name="smugmug-oauth-web-demo",
            consumer_key=key,
            consumer_secret=secret,
            request_token_url=REQUEST_TOKEN_URL,
            access_token_url=ACCESS_TOKEN_URL,
            authorize_url=AUTHORIZE_URL,
            base_url=API_BASE + "/api/v2",
        )


def get_user_session():
    return OAuth1Session(
        APP_KEY, APP_SECRET, access_token=USER_TOKEN, access_token_secret=USER_SECRET,
    )


def setup_auth(cb_url):
    global REQ_TOKEN
    global REQ_SECRET
    REQ_TOKEN, REQ_SECRET = SERVICE.get_request_token(params={"oauth_callback": cb_url})
    return REQ_TOKEN, REQ_SECRET


def verify_callback(oauth_verifier: str) -> bool:
    global USER_TOKEN
    global USER_SECRET

    if SERVICE is None:
        return False

    USER_TOKEN, USER_SECRET = SERVICE.get_access_token(
        REQ_TOKEN, REQ_SECRET, params={"oauth_verifier": oauth_verifier},
    )

    return True
