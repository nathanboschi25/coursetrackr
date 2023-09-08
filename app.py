import locale

from flask import Flask, render_template, request, redirect, g, session, url_for

app = Flask(__name__, template_folder='views', static_folder='static')
app.secret_key = 'une cle(token) : grain de sel(any random string)'


locale.setlocale(locale.LC_ALL, 'french')


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# SECURITY MIDDLEWARE
from controllers.auth_security import auth_security

app.register_blueprint(auth_security)

# CONNECTED PAGES
from controllers.logged_pages import connected

app.register_blueprint(connected, url_prefix='/connected')


@app.route('/routes')
def get_routes():
    print(app.url_map)
    return ""


@app.route('/')
def index():
    return redirect(url_for('connected.dashboard'))


if __name__ == '__main__':
    app.run()
