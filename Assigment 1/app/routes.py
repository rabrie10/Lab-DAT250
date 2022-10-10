#from tkinter import INSERT
from flask import render_template, flash, redirect, url_for, session, request, app#, Flask
from app import app, query_db, queryy_db
from app.forms import IndexForm, PostForm, FriendsForm, ProfileForm, CommentsForm
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import os
<<<<<<< HEAD
import re 
#from flask_session import Session
#from flask import make_response


# import sqlite3
# from sqlite3 import Error


# def create_connection(db_file):
#     conn = None

#     try: 
#         conn = sqlite3.connect(db_file)
#     except Error as e:
#         print(e)
#     return conn

# def select_all_tasks(conn):
#     """
#     Query all rows in the tasks table
#     :param conn: the Connection object
#     :return:
#     """
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM tasks")

#     rows = cur.fetchall()

#     for row in rows:
#         print(row)


# def select_task_by_priority(conn, priority):
#     """
#     Query tasks by priority
#     :param conn: the Connection object
#     :param priority:
#     :return:
#     """
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM Users WHERE priority=?", (priority,))

#     rows = cur.fetchall()

#     for row in rows:
#         print(row)

# database = r"/mnt/c/users/eier/github/Lab-DAT250/'Assigment 1'/database.db"

# conn =create_connection(database)
# with conn:
#     data = select_all_tasks(conn)

# this file contains all the different routes, and the logic for communicating with the database

# home page/login/registration

#@app.before_request
#def require_login():
 #   allowed_routes = ['stream']

# app.config['SESSION_PERMANENT']=False
# app.config['SESSION_TYPE'] = 'filesystem'

# app.config['PERMANENT_SESSION_LIFETIME']=timedelta(minutes=1)
=======
>>>>>>> 8be3c359fbcbcbf58fe1c20b52d83b0b3abe2585


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])


def index():

    form = IndexForm()
    
    
    if form.login.is_submitted() and form.login.submit.data:
        if not re.match("^[a-zA-Z0-9_@]+$", form.login.username.data):
            flash("invalid username")
            return render_template('index.html', title='Welcome', form=form)
        
        user = query_db('SELECT * FROM Users WHERE username="{}";'.format(form.login.username.data), one=True)
        
        

        #user['password']
        #hashedpassword  = generate_password_hash((form.login.password.data), method='sha256')


    #check hashedpassword during login
        if user == None:
            flash('Sorry, this user does not exist!')
        
        elif check_password_hash(user['password'], form.login.password.data) == True:
            session['username'] = user['username']
            #session['username']=user
            #session.permanent=True
            return redirect(url_for('stream', username=form.login.username.data))
        else:
            flash('Sorry, wrong password!')
    elif form.register.is_submitted() and form.register.submit.data:
        if form.register.password.data==form.register.confirm_password.data:
            username = queryy_db('SELECT * From Users', one=True)
            if username == None:
                pass
            else:
                for i in username:
                    a=i[1]
                    if a == form.register.username.data:
                        flash("Username already in use")
                        return redirect(url_for('index'))
                    else:
                        pass
#generating hashed password, fixing confirm password and giving max, min to password and usernames
            if 8 <= int(len(form.register.password.data)) <= 128 and 4 <= int(len(form.register.username.data)) <= 15:
                form.register.password.data = generate_password_hash(form.register.password.data, method='sha256')
                query_db('INSERT INTO Users (username, first_name, last_name, password) VALUES("{}", "{}", "{}", "{}");'.format(form.register.username.data, 
                form.register.first_name.data, form.register.last_name.data, form.register.password.data))
            else:
                flash("Min, max username length: 4,15. min, max password length: 8, 128")

            return redirect(url_for('index'))
        else:
            flash("Confirm password needs to be the same as password...")
    return render_template('index.html', title='Welcome', form=form)

#if anyone tryes to access non-accessible page, send them to index
@app.before_request
def require_login():
    allowed_routes = ['index']
    if request.endpoint not in allowed_routes and 'username' not in session:
    #if 'username' not in session:
       return redirect('/index')



# content stream page
@app.route('/stream/<username>', methods=['GET', 'POST'])
def stream(username):
    form = PostForm()
    user = query_db('SELECT * FROM Users WHERE username="{}";'.format(username), one=True)
    if form.validate_on_submit():
        if form.image.data:
            if form.image.data != None:
                path = os.path.join(app.config['UPLOAD_PATH'], form.image.data.filename)
                form.image.data.save(path)


                query_db('INSERT INTO Posts (u_id, content, image, creation_time) VALUES({}, "{}", "{}", \'{}\');'.format(user['id'], form.content.data, form.image.data.filename, datetime.now()))
            else:
                query_db('INSERT INTO Posts (u_id, content, creation_time) VALUES({}, "{}" \'{}\');'.format(user['id'], form.content.data, datetime.now()))
                flash("Need to post Picture with post!")
                
        return redirect(url_for('stream', username=username))   

    posts = query_db('SELECT p.*, u.*, (SELECT COUNT(*) FROM Comments WHERE p_id=p.id) AS cc FROM Posts AS p JOIN Users AS u ON u.id=p.u_id WHERE p.u_id IN (SELECT u_id FROM Friends WHERE f_id={0}) OR p.u_id IN (SELECT f_id FROM Friends WHERE u_id={0}) OR p.u_id={0} ORDER BY p.creation_time DESC;'.format(user['id']))
    return render_template('stream.html', title='Stream', username=username, form=form, posts=posts)

# comment page for a given post and user.
@app.route('/comments/<username>/<int:p_id>', methods=['GET', 'POST'])
def comments(username, p_id):
    form = CommentsForm()
    if form.is_submitted():
        user = query_db('SELECT * FROM Users WHERE username="{}";'.format(username), one=True)
        query_db('INSERT INTO Comments (p_id, u_id, comment, creation_time) VALUES({}, {}, "{}", \'{}\');'.format(p_id, user['id'], form.comment.data, datetime.now()))

    post = query_db('SELECT * FROM Posts WHERE id={};'.format(p_id), one=True)
    all_comments = query_db('SELECT DISTINCT * FROM Comments AS c JOIN Users AS u ON c.u_id=u.id WHERE c.p_id={} ORDER BY c.creation_time DESC;'.format(p_id))
    return render_template('comments.html', title='Comments', username=username, form=form, post=post, comments=all_comments)

# page for seeing and adding friends
@app.route('/friends/<username>', methods=['GET', 'POST'])
def friends(username):
    form = FriendsForm()
    user = query_db('SELECT * FROM Users WHERE username="{}";'.format(username), one=True)
    if form.is_submitted():
        friend = query_db('SELECT * FROM Users WHERE username="{}";'.format(form.username.data), one=True)
        if friend is None:
            flash('User does not exist')
        elif friend == user:
            flash("You can't add yourself.") 
        
        else:
            query_db('INSERT INTO Friends (u_id, f_id) VALUES({}, {});'.format(user['id'], friend['id']))
    
    all_friends = query_db('SELECT * FROM Friends AS f JOIN Users as u ON f.f_id=u.id WHERE f.u_id={} AND f.f_id!={} ;'.format(user['id'], user['id']))
    return render_template('friends.html', title='Friends', username=username, friends=all_friends, form=form)

# see and edit detailed profile information of a user
@app.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    form = ProfileForm()
    if form.is_submitted():
        query_db('UPDATE Users SET education="{}", employment="{}", music="{}", movie="{}", nationality="{}", birthday=\'{}\' WHERE username="{}" ;'.format(
            form.education.data, form.employment.data, form.music.data, form.movie.data, form.nationality.data, form.birthday.data, username
        ))
        return redirect(url_for('profile', username=username))
    
    user = query_db('SELECT * FROM Users WHERE username="{}";'.format(username), one=True)
    return render_template('profile.html', title='profile', username=username, user=user, form=form)


    