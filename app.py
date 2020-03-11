import functools
import json
import os

from flask import Flask, render_template

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery

import google_auth
from flask.templating import render_template


app = Flask(__name__)

app.secret_key = "SivaRamdom123"

app.register_blueprint(google_auth.app)

@app.route('/',methods = ['POST', 'GET'])
def home():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        r = json.dumps(user_info)
        loaded_r = json.loads(r)
        print(r)
        return render_template("index.html",message='yes',usrimg=loaded_r['picture'],userin=loaded_r['name'])

    return render_template("index.html",message='You are not currently logged in.',userin=None)

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")