from flask import Flask, render_template, request, redirect, url_for, jsonify,session,flash,abort
import json
import os
import  time
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__,template_folder='F:\\2024_code\\software\\teacher_management1\\teacher_management\\templates')
app.secret_key = 'teachermanagement'
from model import Teacher,Appointment
# 假设这是你的登录和注册页面模板
@app.route('/',)
def index():
    # 根据查询参数或其他逻辑决定渲染登录还是注册页面
    return render_template('start.html')

@app.route('/teacher',)
def teacher():
    user_name = session.get('username', 'Guest')  # 如果没有找到name，默认为'Guest'
    user_identify = session.get('identify', 'Unknown')  # 如果没有找到
    user_email = session.get('email','Unknown')
    error_message = request.args.get('error')
    return render_template('teacher.html', name=user_name, identify=user_identify,email=user_email, error_message=error_message)
# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    with open('F:\\2024_code\\software\\teacher_management1\\teacher_management\\register_users.json', 'r') as f:
        users = json.load(f)
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # 查找用户是否存在
        user = next((u for u in users if u['email'] == email), None)
        print(user)

        if user and check_password_hash(user['password'], password):
            session['username'] = username
            session['identify'] = user['identify']
            session['email']=user['email']
            # 登录成功,返回成功信息
            if session['identify'] =="teacher":
                return jsonify({'message': 'login successful,teacher'}), 200
            else:
                return jsonify({'message': 'login successful,student'}), 200
            #return redirect(url_for('menu'))
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
                identify = request.form['identify']
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
                'password': password_hash,
                'identify': identify
            }

            try:
                with open('F:\\2024_code\\software\\teacher_management1\\teacher_management\\register_users.json', 'r') as f:
                    users = json.load(f)
            except FileNotFoundError:
                users = []
            except json.JSONDecodeError:
                print("Error: register_users.json contains invalid JSON data")
                users = []

            users.append(user_data)

            try:
                with open('F:\\2024_code\\software\\teacher_management1\\teacher_management\\register_users.json', 'w') as f:
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
    user_name = session.get('username', 'Guest')  # 如果没有找到name，默认为'Guest'
    user_identify = session.get('identify', 'Unknown')  # 如果没有找到
    user_email =session.get('email','Unknown')
    error_message = request.args.get('error')
    return render_template('menu.html', name=user_name, identify=user_identify, email=user_email , error=error_message)

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
@app.route('/update_teacher', methods=['GET','POST'])
def update_teacher():
    if 'identify' in session and session['identify'] == 'teacher':
        # 用户是老师，允许访问更新页面
        teachers = Teacher.load_teachers()
        if request.method == 'POST':
            data = request.json
            id = int(data.get('id'))    
            new = 1
            name = data.get('name')
            academy = data.get('academy')
            url = data.get('url')
            information = data.get('info')
            email=data.get('email')
            # 找到要更新的教师对象
            for teacher in teachers:
                if str(teacher["email"]) == str(email):
                    print("成功匹配")
                    teacher["name"] = name
                    teacher["academy"] = academy
                    teacher["url"] = url
                    teacher['information'] = information
                    teacher['email']=email
                    new = 0
                    break
            if new == 0:
                if 'email' in session and session['email'] == email:
                    Teacher.save_teachers(teachers)
                    return jsonify({"message": "update successfully"}), 203
            else:
                teacher1 = {}
                teacher1["id"] = int(id)
                teacher1["name"] = name
                teacher1["academy"] = academy
                teacher1["url"] = url
                teacher1['information'] = information
                teacher1['times'] = str(0)
                teacher1['email'] = email
                teachers.append(teacher1)
                print(teachers)
                Teacher.save_teachers(teachers)
                return jsonify({"success": "add successfully"}), 200

            # 保存更新后的教师数据

        else:
            for teacher in teachers:
                if teacher["email"] == session['email']:
                    teacher_update=teacher
                    print("要更新的教师信息")
                    print(teacher_update)
                    break
            teacher_information=teacher_update['information']
            print(teacher_information)
            return render_template('update.html',teacher_update=teacher_update,teacher_information=teacher_information)  # return redirect(url_for('index'))
    else:
        # 用户不是老师或者没有登录，显示错误消息并重定向
        return redirect(url_for('menu', error='no_permission'))


@app.route('/teacher/<int:teacher_id>/book', methods=['GET', 'POST'])
def book_teacher(teacher_id):
    if request.method == 'POST':
        data = request.json

        # 检查时间冲突的逻辑（已注释）
        # if Appointment.check_conflict(teacher_id, data.get('date'), data.get('time')):
        #     return jsonify({"error": "Time conflict, please choose another time"}), 409
        appointment_id = str(int(time.time() * 1000))
        # 构造字典
        appointment_dict = {
            'studentName': data.get('studentName'),
            'studentEmail':data.get('studentEmail'),
            'academy': data.get('academy'),
            'purpose': data.get('purpose'),
            'teacherId': teacher_id,
            'date': data.get('date'),
            'time': data.get('time'),
            'appointment_id':appointment_id,
            'is_accepted': False
        }
        print(appointment_dict)

        try:
            appointments = Appointment.load_appointments()
            appointments.append(appointment_dict)
        except json.decoder.JSONDecodeError:
            appointments = []
            appointments.append(appointment_dict)

        Appointment.save_appointment(appointments)

        return jsonify({"message": "预约信息已经发给教师，等待确认", "appointment": appointment_dict}), 201

    else:
        return render_template('book.html',teacher_id=teacher_id)
@app.route('/teacher/<int:teacher_id>/schedule', methods=['GET'])
def get_teacher_schedule(teacher_id):
    teachers = Teacher.load_teachers()
    teacher = Teacher.get_teacher_by_id(teacher_id, teachers)
    if teacher:
        # 假设我们只返回第一个教师的日程信息
        teacher = Teacher.get_teacher_by_id(teacher_id, teachers)
        print(teacher)
        teacher_schedule = teacher[0]["schedule"]
        return render_template('schedule.html',schedule=teacher_schedule)

    else:
        return jsonify({"error": "Teacher not found"}), 404
@app.route('/teacher/<string:email>/schedule_update', methods=['GET', 'POST'])
def update_teacher_schedule(email):
    user_name = session.get('username', 'Guest')  # 如果没有找到name，默认为'Guest'
    user_identify = session.get('identify', 'Unknown')  # 如果没有找到
    user_email =session.get('email','Unknown')
    error_message = request.args.get('error')
    teachers = Teacher.load_teachers()
    if request.method == 'POST':
        teacher = Teacher.get_teacher_by_email(user_email, teachers)
        print(teacher)
        if teacher:
            # 假设请求的数据格式是 {'schedule': [{'date': '...', 'time': '...', 'event': '...'}]}
            data = request.json
            if 'schedule' in teacher:
                schedule_teacher=data.get('schedule')
                teacher['schedule'].append(schedule_teacher[0])
                Teacher.save_teachers(teachers)
                return jsonify({"message": "Schedule updated successfully"}), 200
            else:
                teacher['schedule'] = data.get('schedule')
                Teacher.save_teachers(teachers)
                return jsonify({"message": "Schedule updated successfully"}), 200
        else:
            return jsonify({"error": "Teacher not found"}), 404
    else:
        return render_template('schedule_update.html',teacher_name=user_name, identify=user_identify,email=user_email, error_message=error_message)
    

@app.route('/menu/<string:student_email>/viewappointment', methods=['GET', 'POST'])
def view(student_email):
    user_name = session.get('username', 'Guest')  # 如果没有找到name，默认为'Guest'
    user_identify = session.get('identify', 'Unknown')  # 如果没有找到
    error_message = request.args.get('error')
    user_email=session.get('email','Unknown')
    all = Appointment.load_appointments()
    result = []
    for each in all:
        if each["studentEmail"] == user_email:
            result.append(each)
    if result==[]:
        return jsonify({"message": "no appointment"}), 200
    else:
        return render_template('viewappointment.html',result=result)


@app.route('/get-appointments/<string:teacheremail>', methods=['GET'])
def get_appointments(teacheremail):
    # user_email=session.get('email')
    appointments_load=Appointment.load_appointments()
    teacher_data = Teacher.load_teachers()
    # 过滤出当前教师的预约信息
    if request.method=='GET':
        appointments = []
        teacher_id = Teacher.get_teacher_by_email(teacheremail, teacher_data)['id']
        print("teacher_id:",teacher_id)
        new = 0
        for app in appointments_load:
            if app["teacherId"] == teacher_id:
                appointments.append(app)
                if app["is_accepted"] == False:
                    new = 1
        # 检查是否有新的预约
        if new == 1:
            print("有未确认的预约信息")
            # 更新上一次的预约列表
            print(appointments)
        return render_template('teacher_check.html', email=teacheremail, result=appointments)
    # if request.method=='POST':
    #     data = request.get_json()
    #     teacher_data = Teacher.load_teachers()
    #     appointment_id = data.get('appointment_id')
    #     teacher_id = Teacher.get_teacher_by_email(user_email, teacher_data)['id']
    #     print("appointment_id:", appointment_id)
    #     appointments = Appointment.load_appointments()
    #     for appointment in appointments:
    #         if appointment['appointment_id'] == appointment_id and appointment['teacherId'] == teacher_id:
    #             appointment['is_accepted'] = True
    #             break
    #     else:
    #         # 如果预约不存在或不属于该教师
    #         abort(404, description="Appointment not found or does not belong to the teacher")

    #     Appointment.save_appointment(appointments)

    #     return jsonify({"message": "Appointment accepted successfully"})



@app.route('/accept-appointment/<string:teacheremail>', methods=['POST'])
def accept_appointment(teacheremail):
    #data = request.get_json()
    # teacher_data=Teacher.load_teachers()
    appointment_id = request.form.get('appointment_id')
    # and appointment['teacherId'] == teacher_id
    # teacher_id = Teacher.get_teacher_by_email(teacheremail,teacher_data)['id']
    print("appointment_id:",appointment_id)
    appointments = Appointment.load_appointments()
    for appointment in appointments:
        if appointment['appointment_id'] == appointment_id :
            if appointment['is_accepted'] != True:
                appointment['is_accepted'] = True
                # 操作成功后，使用flash发送消息
                flash('Appointment accepted successfully', 'success')
                break
            elif appointment['is_accepted'] == True:
                flash('Appointment has been accepted ', 'success')
                break

    else:
        # 如果预约不存在或不属于该教师
        abort(404, description="Appointment not found or does not belong to the teacher")

    Appointment.save_appointment(appointments)


    # user_email=session.get('email')
    appointments_load=Appointment.load_appointments()
    teacher_data = Teacher.load_teachers()
    appointments = []
    teacher_id = Teacher.get_teacher_by_email(teacheremail, teacher_data)['id']
    print("teacher_id:",teacher_id)
    new = 0
    for app in appointments_load:
        if app["teacherId"] == teacher_id:
            appointments.append(app)  
    return render_template('teacher_check.html', email=teacheremail, result=appointments)


# 运行 Flask 应用
if __name__ == '__main__':
    app.run(debug=True)