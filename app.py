import os
from urllib.parse import urlparse, parse_qs

from flask import Flask, render_template, request, redirect

import oauth
from utils import fix_auth_url

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]


def has_access() -> bool:
    return has_keys() and oauth.USER_TOKEN is not None and oauth.USER_SECRET is not None


def has_keys() -> bool:
    return oauth.APP_KEY is not None and oauth.APP_SECRET is not None


@app.route("/", methods=["GET"])
def index():
    if has_access():
        return render_template(
            "test.html", token=oauth.USER_TOKEN, secret=oauth.USER_SECRET,
        )
    elif has_keys():
        return render_template("auth.html")
    else:
        return render_template("index.html")


@app.route("/auth", methods=["GET", "POST"])
def auth():
    if request.method == "POST":
        oauth.setup_service(request.form["key"], request.form["secret"])

    oauth.setup_auth("{}callback".format(request.host_url))

    auth_url = fix_auth_url(oauth.SERVICE.get_authorize_url(oauth.REQ_TOKEN))
    return redirect(auth_url)


@app.route("/callback", methods=["GET"])
def callback():
    oauth.verify_callback(request.args.get("oauth_verifier"))
    return redirect("/")


@app.route("/test", methods=["GET", "POST"])
def test():
    user_session = oauth.get_user_session()
    json = make_api_request(user_session, request.args.get("path"))
    return render_template(
        "test.html", token=oauth.USER_TOKEN, secret=oauth.USER_SECRET, json=json,
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
