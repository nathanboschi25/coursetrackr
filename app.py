import locale

from flask import Flask, redirect, g, url_for

app = Flask(__name__, template_folder='views', static_folder='static')
app.secret_key = 'une cle(token) : grain de sel(any random string)'


locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


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

# TEACHER PAGES
from controllers.teacher_pages import teachers

app.register_blueprint(teachers, url_prefix='/teachers')

# ADE UPDATE
from controllers.ade_update import ade_update
app.register_blueprint(ade_update, url_prefix='/ade')


@app.route('/routes')
def get_routes():
    print(app.url_map)
    return ""


@app.route('/')
def index():
    return redirect(url_for('connected.dashboard'))



if __name__ == '__main__':
    app.run()
