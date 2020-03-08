# Python standard libraries
import json
import os
import sqlite3
from datetime import datetime
import re

# Third-party libraries
from flask import Flask, redirect, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests
import pprint
from bs4 import BeautifulSoup
from flask import Flask, render_template

# Internal imports
from db import init_db_command
from user import User


app = Flask(__name__)


#res = requests.get('https://news.ycombinator.com/news')

#res.proxies = {
#    "http": "10.142.125.36:8080",
#    "https": "10.142.125.36:8080"
#}

soup = BeautifulSoup(res.text, "html.parser")
links = soup.select(".storylink")
subtext = soup.select(".subtext")


def sort_stories_by_vote(hackli):
    return sorted(hackli, key=lambda k: k['votes'], reverse=True)


def create_custom_hm(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = links[idx].getText()
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_vote(hn)


columns = create_custom_hm(links, subtext)


@app.route("/")
def home():
    return render_template("index.html", columns=['title', 'link', 'votes'], items=columns)

# New functions
@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/contact/")
def contact():
    return render_template("contact.html")
