from flask import Flask, render_template, request, session, redirect, make_response
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
        else:
            return render_template('login.html',
                                   nav_links=get_nav_links(),
                                   display_mode=display_mode,
                                   error='')
    elif request.method == 'POST':
        form_data = request.form
        user = ""
        password = ""
        for key, value in form_data.items():
            if key == "user":
                user = value
            if key == "pass":
                password = value
        if authenticate(user, password):
            session['loggedIn'] = True
            return redirect('/preferences/')
        else:
            return render_template('login.html',
                                   nav_links=get_nav_links(),
                                   display_mode=display_mode,
                                   error='Authentication failed. Please try again.')
    else:
        raise NotImplementedError('Request method not implemented: ' + request.method)


@app.route('/logout/')
def logout():
    display_mode = cookie_update(request.cookies)
    if session['loggedIn']:
        session['loggedIn'] = False
        return render_template('logout.html',
                               nav_links=get_nav_links(),
                               display_mode=display_mode)
    else:
        return render_template('error.html',
                               nav_links=get_nav_links(),
                               display_mode=display_mode,
                               error='You are not logged in')


@app.route('/preferences/', methods=['POST', 'GET'])
def preferences():
    set_display_mode = ''
    if request.method == 'POST':
        if request.form['submit_button'] == 'Light Mode':
            set_display_mode = 'light'
        elif request.form['submit_button'] == 'Dark Mode':
            set_display_mode = 'dark'
        else:
            pass  # unknown
    display_mode = cookie_update(request.cookies, set_display_mode)
    if session['loggedIn']:
        res = make_response(
            render_template('preferences.html',
                            nav_links=get_nav_links(),
                            display_mode=display_mode))
        if set_display_mode != '':
            res.set_cookie('displayMode', set_display_mode, max_age=60 * 60 * 24 * 3)
        return res
    else:
        return render_template('error.html',
                               nav_links=get_nav_links(),
                               display_mode=display_mode,
                               error='You must be logged in to view this page.')


def authenticate(user, password):
    return user == 'CIS658' and password == 'WebArchitectures'


def get_nav_links():
    if session['loggedIn']:
        return {
            "Home": "/",
            "Log Out": "/logout",
            "Preferences": "/preferences"
        }
    else:
        return {
            "Home": "/",
            "Login": "/login"
        }


def get_articles():
    return {
        "Blog post 1": paragraph(),
        "Blog post 2": paragraph(),
        "Blog post 3": paragraph(),
    }


def cookie_update(cookies, display_override=''):
    if 'loggedIn' not in session:
        session['loggedIn'] = False
    if display_override != '':
        return display_override
    display_mode = 'light'
    if cookies.get('displayMode') == 'dark':
        display_mode = 'dark'
    return display_mode


if __name__ == "__main__":
    app.secret_key = "ThisIsAVerySecretSecretKey"
    app.run(host='0.0.0.0', port=8000)
