import flask
import requests


app = flask.Flask(__name__)
app.debug = False


def _serve_url_contents_as_text(url):
    response = flask.make_response(requests.get(url).text)
    response.headers['content-type'] = 'text/plain'
    return response


@app.route('/stable')
def stable():
    return _serve_url_contents_as_text(
            'https://raw.github.com/rconradharris/bashfiles/stable/bashfiles')


def _master():
    return _serve_url_contents_as_text(
            'https://raw.github.com/rconradharris/bashfiles/master/bashfiles')


@app.route('/master')
def master():
    return master()


@app.route('/latest')
def latest():
    return _master()


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
        return flask.redirect('https://github.com/rconradharris/bashfiles')
