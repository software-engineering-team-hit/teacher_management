from flask import Flask, request, jsonify ,render_template
import json

app = Flask(__name__,template_folder='F:\\2024_code\\software\\teacher_management\\templates')

@app.route('/register', methods=['GET', 'POST'])
def register():
    print("Entering register() function")
    if request.method == 'POST':
        print("Received POST request")
        # 获取表单数据
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # 将用户信息存储到 JSON 文件
        user_data = {
            'username': username,
            'email': email,
            'password': password
        }

        try:
            with open('register_users.json', 'r') as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []

        users.append(user_data)

        with open('register_users.json', 'w') as f:
            json.dump(users, f)

        # 返回 JSON 格式的注册成功响应
        return jsonify({'message': 'Registration successful!'})
    
    print("Rendering register.html template")
    # 如果是 GET 请求,则渲染注册页面模板
    return render_template('register.html')

if __name__ == '__main__':
    print("Starting Flask application")
    app.run()