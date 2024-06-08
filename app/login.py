from flask import Flask, render_template, request, jsonify
import json
from werkzeug.security import check_password_hash

app = Flask(__name__,template_folder='F:\\2024_code\\software\\teacher_management\\templates')

# 从 user.json 文件中读取用户数据
with open('register_users.json', 'r') as f:
    users = json.load(f)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    # 获取登录表单数据
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # 查找用户是否存在
    user = next((u for u in users if u['username'] == username), None)
    print(user)

    if user and check_password_hash(user['password'], password):
        # 登录成功,返回成功信息
        return jsonify({'message': 'Login successful'})
    elif user:
        # 用户名存在但密码错误
        return jsonify({'message': 'Invalid password'}), 401
    else:
        # 用户名不存在
        return jsonify({'message': 'User does not exist'}), 404

if __name__ == '__main__':
    app.run(debug=True)