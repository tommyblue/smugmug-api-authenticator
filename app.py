from urllib.parse import urlparse, parse_qs

from flask import Flask, render_template, request, redirect, make_response

import oauth
from utils import fix_auth_url

app = Flask(__name__)


def has_access() -> bool:
    return (
        has_app_keys()
        and request.cookies.get("user_token") is not None
        and request.cookies.get("user_secret") is not None
    )


def has_app_keys() -> bool:
    return (
        request.cookies.get("app_key") is not None
        and request.cookies.get("app_secret") is not None
    )


@app.route("/", methods=["GET"])
def index():
    if has_access():
        return render_template(
            "test.html",
            token=request.cookies.get("user_token"),
            secret=request.cookies.get("user_secret"),
        )
    else:
        return render_template("index.html")


@app.route("/auth", methods=["POST"])
def auth():
    key = request.form["key"]
    secret = request.form["secret"]
    oauth.setup_service(key, secret)

    req_token, req_secret = oauth.setup_auth("{}callback".format(request.host_url))
    auth_url = fix_auth_url(oauth.SERVICE.get_authorize_url(req_token))

    resp = make_response(redirect(auth_url))
    resp.set_cookie("app_key", key)
    resp.set_cookie("app_secret", secret)
    resp.set_cookie("req_token", req_token)
    resp.set_cookie("req_secret", req_secret)

    return resp


@app.route("/callback", methods=["GET"])
def callback():
    user_token, user_secret = oauth.verify_callback(
        request.args.get("oauth_verifier"),
        request.cookies.get("req_token"),
        request.cookies.get("req_secret"),
    )

    resp = make_response(redirect("/"))
    resp.set_cookie("user_token", user_token)
    resp.set_cookie("user_secret", user_secret)

    return resp


@app.route("/test", methods=["GET", "POST"])
def test():
    user_session = oauth.get_user_session(
        request.cookies.get("app_key"),
        request.cookies.get("app_secret"),
        request.cookies.get("user_token"),
        request.cookies.get("user_secret"),
    )
    json = make_api_request(user_session, request.args.get("path"))
    return render_template(
        "test.html",
        token=request.cookies.get("user_token"),
        secret=request.cookies.get("user_secret"),
        json=json,
    )


def make_api_request(session, input_path) -> str:
    parsed = urlparse(input_path)
    params = parse_qs(parsed.query)
    params["_pretty"] = ""
    return session.get(
        oauth.API_BASE + parsed.path,
        params=params,
        headers={"Accept": "application/json"},
    ).text
