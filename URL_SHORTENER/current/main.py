import random
import string
import json
from flask import Flask, render_template, redirect, request, url_for
import webbrowser

app = Flask(__name__, template_folder='templates')

shortened_urls = {}


def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join((random.choice(chars)) for _ in range(length))
    return short_url


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()

        shortened_urls[short_url] = long_url
        with open("urls.json", "w") as f:
            json.dump(shortened_urls, f)
        return render_template("shortened_url.html", short_url=request.url_root + short_url)
    return render_template("index.html")


@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        return redirect(long_url)  # Redirect to the target URL
    else:
        return "URL NOT FOUND", 404


if __name__ == "__main__":
    with open("urls.json", "r") as f:
        shortened_urls = json.load(f)
    webbrowser.open_new_tab('http://127.0.0.1:5000/')
    app.run(debug=True)
