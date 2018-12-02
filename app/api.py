from app import app, db
from flask import request,g,abort,jsonify
import json
from models import User,Post
from authen.authenticate import authen_token, set_token
from authen.gen import generate_token
from danger import encrypt_password, validate_password
from hotdata.codeInfo import *

def authen_validate(request):
    user_id = int(request.cookies.get('user_id',None))
    token = request.cookies.get('access_token',None)
    return authen_token(user_id, token)

@app.route('/protected',methods=['POST'])
def protected():    
    if not authen_validate(request):
        abort(400)
    return 'success'


@app.route('/api_v1/login',methods=['POST'])
def api_login():
    username = request.json.get('username',None)
    password = request.json.get('password', None)
    if username == None or password == None:
        abort(400)
    user = User.query.filter_by(username = username).first()
    if user == None:
        abort(400)
    
    hashed = user.password

    hashed_thistime = encrypt_password(password).decode('utf8')
    if hashed == hashed_thistime:
        token = generate_token(user.username)
        set_token(user.user_id, token)
        return json.dumps( {'access_token':token, 'user_id':user.user_id, 'username':username})
    else:
        return json.dumps({'status':'failed'})

    
    


@app.route('/api_v1/users',methods=['POST'])
def api_adduser():
    username = request.json.get('username',None)
    password = request.json.get('password', None)

    if username == None or password == None:
        abort(400)
    user = User.query.filter_by(username = username).first()
    if user != None:
        return json.dumps({'status':'user exists'})

    hashpwd = encrypt_password(password)
    new_user = User(username=username,password=hashpwd)
    
    db.session.add(new_user)
    db.session.commit()
    token = generate_token(username)
    set_token(new_user.user_id, token)
    return json.dumps({'user_id':new_user.user_id, 'access_token':token})



@app.route('/api_v1/posts',methods=['POST'])
def api_pubpost():    
    if not authen_validate(request):
            abort(400)
    content = request.json.get('content')
    user_id = request.json.get('user_id')
    title = request.json.get('title')
    username = request.json.get('username')
    post = Post(user_id=user_id, username=username, content=content, title=title)
    print('title :', title)
    db.session.add(post)
    db.session.commit()
    return json.dumps({'status':'sucess'})
    
@app.route('/api_v1/posts',methods=['PUT'])
def api_modifypost():
    if not authen_validate(request):
            abort(400)
    content = request.json.get('content')
    user_id = request.json.get('user_id')
    title = request.json.get('title')
    username = request.json.get('username')
    print(title)
    print(username)
    post = Post.query.filter_by(title=title,username=username).first()
    print(post)
    post.content = content
    db.session.add(post)
    db.session.commit()
    return json.dumps({'status':'success'})


@app.route('/api_v1/codeInfo',methods=['POST'])
def api_codeinfo(): 
    username = request.json.get('username')
    user = User.query.filter_by(username = username).first()
    if user == None:
        abort(404)
    user_id = user.user_id
    print('================')
    print(user_id)
    print("="*20)
    infotype = request.json.get('infotype')

    if infotype == 'language':
        language = get_code_info(user_id)
        if not language:
            
            return json.dumps( {'status':'notexist', 'test':1} )
        return language
    
    
