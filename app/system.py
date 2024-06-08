from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__,template_folder='E:\\csnerwork\\teacher_management\\templates')
from model import Teacher
# 假设这是你的登录和注册页面模板
@app.route('/',)
def index():
    # 根据查询参数或其他逻辑决定渲染登录还是注册页面
    return render_template('start.html')

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    with open('E:\\csnerwork\\teacher_management\\register_users.json', 'r') as f:
        users = json.load(f)
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # 查找用户是否存在
        user = next((u for u in users if u['username'] == username), None)
        print(user)

        if user and check_password_hash(user['password'], password):
            # 登录成功,返回成功信息
            #return jsonify({'message': 'login successful'}), 200
            return redirect(url_for('menu'))
        elif user:
            # 用户名存在但密码错误
            return jsonify({'message': 'Invalid password'}), 401
        else:
            # 用户名不存在
            return jsonify({'message': 'User does not exist'}), 404

    else:
        # GET 请求，渲染登录页面
        return render_template('login.html')

# 注册路由
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.method == 'POST':
            # 获取表单数据
            try:
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']
            # 异常处理 如果前端传来的数据格式有问题,引发 KeyError 或 TypeError 异常
            except (KeyError, TypeError):
                return jsonify({'message': 'Invalid registration data'}), 400

            # 检查用户是否已经存在

            # 对密码进行加密
            password_hash = generate_password_hash(password)

            # 将用户信息存储到 JSON 文件

            user_data = {
                'username': username,
                'email': email,
                'password': password_hash
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
        #return jsonify({'url': '/login'})
    else:
        # GET 请求，渲染注册页面
        return render_template('register.html')

# 菜单路由
@app.route('/menu',methods=['GET','POST'])
def menu():
    return render_template('menu.html')

# 搜索路由
@app.route('/search')
def search():
    return render_template('search.html')
@app.route('/search/get_teacher_by_id/<int:id>')
def get_teacher_by_id(id):
        # 根据教师ID查询
    teachers_data = Teacher.load_teachers()
    teacher = Teacher.get_teacher_by_id(id, teachers_data)
    if teacher:
        return jsonify(teacher)
    else:
        return jsonify({"error": "Teacher not found"}), 404

@app.route('/search/get_teacher_by_name/<string:name>')
def get_teacher_by_name(name):
    # 根据教师姓名查询
    teachers_data = Teacher.load_teachers()
    teacher = Teacher.get_teacher_by_name(name, teachers_data)
    if teacher:
        return jsonify(teacher)
    else:
        return jsonify({"error": "Teacher not found"}), 404

@app.route('/search/get_teacher_by_academy/<string:academy>')
def get_teacher_by_academy(academy):
    # 根据学院查询
    teachers_data = Teacher.load_teachers()
    teachers = Teacher.get_teacher_by_academy(academy, teachers_data)
    if teachers:
        return jsonify(teachers)
    else:
        return jsonify({"error": "Teachers not found"}), 404
# 特定搜索方式的路由


# 运行 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)