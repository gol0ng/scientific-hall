from flask import Flask, render_template, request, redirect, session, jsonify, send_from_directory

from db import userdataf,scheduledataf,postsdataf
from utils import e_mail

app = Flask(__name__)
app.secret_key = 'kechuangguangchang'

@app.route('/')
def index():
    if session.get('username'):
        avatar = userdataf.get_user(session.get('username'))['avatar']
        avatar = "./static/images/avatar/"+avatar
    else:
        avatar = './static/images/system/default_avatar.png'
    return render_template('index.html',avatar = avatar)

# 注册
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['e_mail']
        password = request.form['password']
        name = request.form['name']
        major = request.form['major']
        job = request.form['job']
        e_mail = request.form['e_mail']
        introduction = request.form['introduction']
        avatar = request.files['avatar']
        if avatar.filename:
            avatar.save('./static/images/avatar/' + avatar.filename)
        userdataf.add_user(username, password, name, avatar.filename, major, job, e_mail, introduction)
        scheduledataf.add_schedule(username)
        return render_template('login.html')

# 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 如果用户已登录，则直接跳转到主页
    if request.method == 'GET':
        if session.get('username'):
            return redirect('/homepage')
        return render_template('login.html')
    # 处理登录请求
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = userdataf.get_user(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect('/')
        else:
            return render_template('login.html', error='用户名或密码错误')
@app.route('/homepage', methods=['GET'])
def homepage():
    if session.get('username'):
        username = session.get('username')
        user = userdataf.get_user(username)
        if session.get('username'):
            avatar = userdataf.get_user(session.get('username'))['avatar']
            avatar = "./static/images/avatar/" + avatar
        else:
            avatar = './static/images/system/default_avatar.png'
        return render_template('homepage.html', user=user, avatar = avatar)
    return render_template('homepage.html')
@app.route('/posts')
def post():
    if session.get('username'):
        avatar = userdataf.get_user(session.get('username'))['avatar']
        avatar = "./static/images/avatar/" + avatar
    else:
        avatar = './static/images/system/default_avatar.png'
    posts = postsdataf.get_all_posts()
    return render_template('posts.html',avatar = avatar,posts = posts)
# 帖子的具体页面
@app.route('/post/<int:post_id>')
def postdetail(post_id):
    if session.get('username'):
        avatar = userdataf.get_user(session.get('username'))['avatar']
        avatar = "../static/images/avatar/" + avatar
    else:
        avatar = '../static/images/system/default_avatar.png'
        return render_template('403.html',avatar = avatar)
    post = postsdataf.get_post(post_id)
    author = userdataf.get_user_by_id(post['author'])
    author_avatar = "../static/images/avatar/" + author['avatar']
    return render_template('postdetail.html', post=post, avatar=avatar, author=author, author_avatar=author_avatar)


@app.route('/search/<string:query>')
def search(query):
    if session.get('username'):
        avatar = userdataf.get_user(session.get('username'))['avatar']
        avatar = "../static/images/avatar/" + avatar
    else:
        avatar = '../static/images/system/default_avatar.png'
    if query:
        users = userdataf.get_user_almost(query)
        return render_template('search.html', users=users,avatar = avatar)

@app.route('/search/')
def search_empty():
    if session.get('username'):
        avatar = userdataf.get_user(session.get('username'))['avatar']
        avatar = "../static/images/avatar/" + avatar
    else:
        avatar = '../static/images/system/default_avatar.png'
    return render_template('404.html',avatar = avatar)

@app.route('/user/<int:id>')
def user(id):
    username = userdataf.get_user_by_id(id)['username']
    user = userdataf.get_user_by_id(id)
    if session.get('username'):
        avatar = userdataf.get_user(session.get('username'))['avatar']
        avatar = "../static/images/avatar/" + avatar
    else:
        avatar = '../static/images/system/default_avatar.png'
    return render_template('user.html', user=user, avatar=avatar)

@app.route('/avatar/<filename>')
def useravatar(filename):
    return send_from_directory('./static/images/avatar', filename)

@app.route('/chat')
def chat():
    return render_template('chat_ai.html')
@app.route('/rank')
def rank():
    return render_template('rank.html')
@app.route('/news')
def news():
    return render_template('404.html')
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')
# 处理日程表
@app.route('/schedule_update', methods=['POST'])
def schedule_add():
    if request.method == 'POST':
        username = session.get('username')
        if username:
            print('username:', username)
            data = request.json
            time = data.get('time')
            print(time)
            content = data.get('content')
            scheduledataf.add_schedule_data(username, time, content)
            return redirect('/')
        else:
            return render_template('login.html', error='请先登录')
@app.route('/schedule_get', methods=['GET'])
def schedule_get():
    if request.method == 'GET':
        username = session.get('username')
        if username:
            schedule_data = scheduledataf.get_schedule_data(username)
            return jsonify(schedule_data[0])
        else:
            schedule_data = scheduledataf.get_schedule_data('empty')
            return jsonify(schedule_data[0])
@app.route('/schedule_get/<int:user_id>', methods=['GET'])
def schedule_get_others(user_id):
    if request.method == 'GET':
        username = userdataf.get_user_by_id(user_id)['username']
        print(username)
        if username:
            schedule_data = scheduledataf.get_schedule_data(username)
            print('----------------------------------------')
            print(schedule_data)
        else:
            print('========================================')
            schedule_data = scheduledataf.get_schedule_data('empty')
            print(schedule_data)
        return jsonify(schedule_data[0])
@app.route('/confirm', methods=['POST'])
def confirm():
    if request.method == 'POST':
        username = session.get('username')
        if username:
            data = request.json
            day = data['day']
            time = data['hour']
            user_id = data['id']
            sender = userdataf.get_user(username)
            sender_name = sender['name']
            sender_email = sender['e_mail']
            receiver = userdataf.get_user_by_id(user_id)
            receiver_name = receiver['name']
            receiver_email = receiver['e_mail']
            e_mail.send_QQ_email_plain('科创广场预约提醒', str(day), str(time), receiver_email,sender_name,sender_email)
            return jsonify({'message': '邮件发送成功'})
        else:
            return redirect('/login')
app.run(debug=True)