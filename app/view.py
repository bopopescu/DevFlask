from app import app, db
from flask import request,g,abort,render_template,abort
import json
from models import User,Post
from authen.authenticate import authen_token, set_token
from authen.gen import generate_token
from danger import encrypt_password, validate_password
from hotdata.codeInfo import *



@app.route('/index',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/<username>',methods=['GET'])
def view_profile(username):
    try:
        page = int(request.args.get('page'))
    except:
        page = 1
    user = User.query.filter_by(username=username)
    if user == None:
        abort(404)
    
    pagination = Post.query.filter_by(username=username ).order_by(Post.datetime.desc()).paginate(page, per_page=16, error_out = True)
    posts = pagination.items
    for x in posts:
        print(x.title)
    return render_template('userprofile.html',posts=posts)

@app.route('/<username>/<post_title>', methods=['GET'])
def view_post(username, post_title):
    post_title = post_title.replace('-',' ')
    post = Post.query.filter_by(username = username, title=post_title).first()
    if post == None:
        abort(404)
    print(post.title)
    return render_template('read_post.html', content=post.content, title=post.title)


@app.route('/write')
def view_writepost():
    return render_template('write_post.html')

@app.route('/<username>/dashboard')
def view_dashboard(username):
    user = User.query.filter_by(username=username).first()
    if user == None:
        abort(404)
    

    active_time = get_active_time(user.user_id)
    if active_time == None:
        active_time = [0]*1440
    else:
        active_time = tobits(active_time)[:1440]


    return render_template('dashboard.html',active_times=active_time)

def tobits(s):
    result = []
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result