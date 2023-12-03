import random
import string
import json
import os
import logging

from flask import Flask, render_template, redirect, url_for, request



app = Flask(__name__)
shortened_urls = {}

def generate_short_url(length=6):

    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url



@app.route("/", methods=["GET", "POST"])

def index():
    if request.method == "POST":
        long_url = request.form['long_url']
        if long_url.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return render_template("index.html", error="Image URLs are not allowed!")
        short_url = generate_short_url()
        while short_url in shortened_urls:
            short_url = generate_short_url()

        shortened_urls[short_url]=long_url

        app.logger.info(f"Added URL: {long_url} with short URL: {short_url} to shortened_urls")
        with open("urls.json","w") as f:
            print("TEST")
            json.dump(shortened_urls,f)
        #return f"Your shortened URL is: {request.url_root}{short_url}" #root url and the /something
        full_short_url = request.url_root + short_url
        return render_template("index.html", short_url=full_short_url)

    return render_template("index.html")


@app.route("/<short_url>")
def redirect_url(short_url):
    long_url = shortened_urls.get(short_url)
    if long_url:
        app.logger.debug(f"Retrieving URL for short URL: {short_url}")
        return redirect(long_url)

    else:
        #return "URL not found", 404
        error_message = f"URL '{short_url}' not found in shortened URLs."
        logging.error(error_message)  # Log an error message
        return f"URL not found: {short_url}. Please check the entered URL.", 404



if __name__ == "__main__":
    if os.path.exists("urls.json"):
        with open("urls.json", "r") as f:
            shortened_urls = json.load(f)
    else:
        shortened_urls = {}

    #app.run(debug=True)







