import flask
import requests


app = flask.Flask(__name__)
app.debug = False

PROJECT_URL = 'https://github.com/rconradharris/bashfiles'
LATEST_URL = 'https://raw.github.com/rconradharris/bashfiles/master/bashfiles'
STABLE_URL = 'https://raw.github.com/rconradharris/bashfiles/stable/bashfiles'

CACHE = {}


def fetch_url(url):
    return requests.get(url).text


def fetch_and_cache_url(url):
    try:
        return CACHE[url]
    except KeyError:
        pass

    data = fetch_url(url)
    CACHE[url] = data
    return data


def serve_text(text):
    response = flask.make_response(text)
    response.headers['content-type'] = 'text/plain'
    return response


@app.route('/clear-cache', methods=['POST'])
def clear_cache():
    CACHE = {}
    flask.abort(204)


@app.route('/stable')
def stable():
    # Do cache stable
    return serve_text(fetch_and_cache_url(STABLE_URL))


@app.route('/latest')
def latest():
    # Don't cache latest
    return serve_text(fetch_url(LATEST_URL))


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
