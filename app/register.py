from flask import Flask, request, jsonify ,render_template
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__,template_folder='E:\\csnerwork\\teacher_management\\templates')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # 获取表单数据
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            identify = request.form['identify']
        #异常处理 如果前端传来的数据格式有问题,引发 KeyError 或 TypeError 异常
        except (KeyError, TypeError):
            return jsonify({'message': 'Invalid registration data'}), 400
        
        # 检查用户是否已经存在

        
        # 对密码进行加密
        password_hash = generate_password_hash(password)

        # 将用户信息存储到 JSON 文件

        user_data = {
            'username': username,
            'email': email,
            'password': password_hash,
            'identify':identify
        }

        try:
            with open('E:\\csnerwork\\teacher_management\\register_users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []
        except json.JSONDecodeError:
            print("Error: register_users.json contains invalid JSON data")
            users = []

        users.append(user_data)


        try:
            with open('E:\\csnerwork\\teacher_management\\register_users.json', 'w') as f:
                json.dump(users, f)
        except FileNotFoundError:
            print("Error: Unable to write to register_users.json file")
        # 返回 JSON 格式的注册成功响应
            
    return jsonify({'message': 'Registration successful!'})

    
    # 如果是 GET 请求,则渲染注册页面模板
@app.route('/', methods=['GET', 'POST'])
def register():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)

