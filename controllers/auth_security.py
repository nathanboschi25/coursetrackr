#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint, url_for
from flask import request, render_template, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from controllers.db_connection import get_db
from models.signature_list import ListeDAO

auth_security = Blueprint('auth_security', __name__,
                          template_folder='templates')


@auth_security.route('/login')
def auth_login():
    return render_template('auth/login.html')


@auth_security.route('/login', methods=['POST'])
def auth_login_post():
    mycursor = get_db().cursor()
    username = request.form.get('username')
    password = request.form.get('password')

    mycursor.execute('''SELECT * FROM users WHERE username=%s''', username)
    user = mycursor.fetchone()

    if user:
        if not check_password_hash(user['password'], password):
            print("password incorrect")
            flash(u'Vérifier votre mot de passe et essayer encore.', 'alert-warning')
            return redirect('/login')
        else:
            session['username'] = user['username']
            session['user_id'] = user['user_id']
            session['name'] = user['name']
            return redirect(url_for('connected.dashboard'))
    else:
        print("login incorrect")
        flash(u'Vérifier votre login et essayer encore.', 'alert-warning')
        return redirect(url_for('auth_security.auth_login'))


@auth_security.route('/signup')
def auth_signup():
    return render_template('auth/signup.html', listes=ListeDAO.get_listes())


@auth_security.route('/signup', methods=['POST'])
def auth_signup_post():
    with get_db().cursor() as mycursor:
        username = request.form.get('username')
        password = request.form.get('password')
        name = request.form.get('name')
        sign_list = request.form.get('signature_list')

        mycursor.execute("SELECT * FROM users WHERE username=%s", username)

        if mycursor.fetchone() is not None:
            flash(u'votre adresse Email ou  votre Login existe déjà', 'alert-warning')
            return redirect(url_for('auth_security.auth_login'))

        # ajouter un nouveau user
        password = generate_password_hash(password, method='sha256')

        mycursor.execute("INSERT INTO users(username, name, password, list_id) VALUE (%s, %s, %s, %s)", (username, name, password))
        get_db().commit()

        mycursor.execute("SELECT LAST_INSERT_ID() AS last_insert_id FROM users")

        user_id = mycursor.fetchone()['last_insert_id']

        session.pop('username', None)
        session.pop('name', None)
        session.pop('user_id', None)
        session['username'] = username
        session['name'] = name
        session['user_id'] = user_id

        return redirect(url_for('connected.dashboard'))


@auth_security.route('/logout')
def auth_logout():
    session.pop('username', None)
    session.pop('name', None)
    session.pop('user_id', None)
    return redirect(url_for('auth_security.auth_login'))

@auth_security.route('/user/edit', methods=['POST'])
def update_user():
    with get_db().cursor() as cursor:
        cursor.execute('UPDATE users SET name=%s, list_id=%s WHERE user_id=%s', (request.form.get('name'), request.form.get('signature_list'), session['user_id']))
        session['name'] = request.form.get('name')
        get_db().commit()
    return redirect(url_for('connected.settings'))
