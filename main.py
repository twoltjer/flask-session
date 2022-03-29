from flask import Flask, render_template, request, session, redirect
from lorem import paragraph

app = Flask(__name__)


@app.route("/")
def homepage():
    display_mode = cookie_update(request.cookies)
    return render_template('homepage.html',
                           nav_links=get_nav_links(),
                           display_mode=display_mode,
                           articles=get_articles())


@app.route("/login", methods=['POST', 'GET'])
def login():
    display_mode = cookie_update(request.cookies)
    if request.method == 'GET':
        if session['loggedIn']:
            return redirect("/")






def get_nav_links():
    return {
        "Home": "/",
        # "Gallery": "/gallery",
        # "Contact Us": "/contact"
    }


def get_articles():
    return {
        "Blog post 1": paragraph(),
        "Blog post 2": paragraph(),
        "Blog post 3": paragraph(),
    }


def cookie_update(cookies):
    if 'loggedIn' not in session:
        session['loggedIn'] = False
    display_mode = 'light'
    if cookies.get('displayMode') == 'dark':
        display_mode = 'dark'
    return display_mode


if __name__ == "__main__":
    app.secret_key = "ThisIsAVerySecretSecretKey"
    app.run(host='0.0.0.0', port=8000)
