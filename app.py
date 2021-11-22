import json
from flask import Flask
from lib import create_client, get_reading_level

app = Flask(__name__)


@app.route("/")
def index():
    return """
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <script>
    function handleSubmit() {
        event.preventDefault();
        location.href='/readability/' + document.forms[0].elements.username.value;
    }
    </script>
    <form onsubmit="handleSubmit()">
        <input type=text name=username>
        <input type=submit>
    </form>
    """


@app.route("/readability/<username>")
def readability(username):
    client = create_client()
    results = get_reading_level(client, username)
    return json.dumps(results)
