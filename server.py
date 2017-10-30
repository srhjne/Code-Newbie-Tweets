import json
import oauth2 as oauth
from secret import keys 
from flask import (Flask, jsonify, render_template)
import pprint #    pp = pprint.PrettyPrinter(indent=4) pp.pprint(stufftoprint)


app = Flask(__name__)
app.secret_key = "miau"


def authorize():
    """authorize w/ twitter api and fetch recent codenewbie tweets, return a json"""

    consumer = oauth.Consumer(key=keys["consumer_key"], secret=keys["consumer_secret"])
    access_token = oauth.Token(key=keys["access_token"], secret=keys["access_secret"])
    client = oauth.Client(consumer, access_token)

    test_url = "https://api.twitter.com/1.1/search/tweets.json?q=%23codenewbie&result_type=mixed&count=100&include_entities=false"
    response, data = client.request(test_url)

    return json.loads(data)


@app.route("/")
def homepage():
    """Display tweets"""
    

    tweet = None
    time_created = None
    retweets = None
    results = authorize()["statuses"]
    output = []

    for result in results:
        tweet = result['text']
        time_created =  result['created_at']
        if 'retweeted_status' in result:
            retweets = result['retweeted_status']['retweet_count']
        output.append((tweet, time_created, retweets))

    return render_template("home.html", output=output)




if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)