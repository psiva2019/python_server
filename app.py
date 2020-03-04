import pprint
from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template
from datetime import datetime
import re

app = Flask(__name__)


res = requests.get('https://news.ycombinator.com/news')

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
