from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

users = []

# 渲染登录页
@app.route('/')
def login():
    return render_template('login.html')

# 处理登录
@app.route('/login', methods=['POST'])
def handle_login():
    key = request.form['key']
    if key == 'miku':  # 替换为你的密钥
        session['logged_in'] = True
        return redirect(url_for('index'))
    else:
        return '密钥错误', 401

# 渲染主页
@app.route('/chat')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

# 处理消息
@socketio.on('message')
def handle_message(msg):
    print(f"Message received: {msg}")
    send(msg, broadcast=True)  # 向所有用户广播消息

# 处理用户加入
@socketio.on('join')
def handle_join(username):
    users.append(username)
    emit('user_list', users, broadcast=True)

# 处理用户断开
@socketio.on('disconnect')
def handle_disconnect():
    for user in users:
        if user == request.sid:
            users.remove(user)
            break
    emit('user_list', users, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='::', port=80, debug=True)
