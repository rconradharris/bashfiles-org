import flask
import requests


app = flask.Flask(__name__)
app.debug = False

PROJECT_URL = 'https://github.com/rconradharris/bashfiles'
LATEST_URL = 'https://raw.github.com/rconradharris/bashfiles/master/bashfiles'
STABLE_URL = 'https://raw.github.com/rconradharris/bashfiles/stable/bashfiles'

CACHE = {}


def fetch_and_cache_url(url):
    try:
        return CACHE[url]
    except KeyError:
        pass

    data = requests.get(url).text
    CACHE[url] = data
    return data


def serve_url(url):
    response = flask.make_response(fetch_and_cache_url(url))
    response.headers['content-type'] = 'text/plain'
    return response


@app.route('/stable')
def stable():
    return serve_url(STABLE_URL)


@app.route('/latest')
def latest():
    return serve_url(LATEST_URL)


@app.route('/bashfiles')
def bashfiles():
    return stable()


@app.route('/')
def index():
    user_agent = flask.request.user_agent.string.lower()
    if user_agent.startswith('curl'):
        return stable()
    elif user_agent.startswith('wget'):
        return stable()
    else:
        return flask.redirect(PROJECT_URL)
