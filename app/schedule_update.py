from flask import Flask, request, jsonify ,render_template
import json
from werkzeug.security import generate_password_hash, check_password_hash
from model import Teacher  # 确保已经导入了修改后的Teacher类

app = Flask(__name__,template_folder='F:\\2024_code\\software\\teacher_management\\templates')


@app.route('/teacher/<int:teacher_id>/schedule_update', methods=['GET', 'POST'])
def update_teacher_schedule(teacher_id):
    teachers = Teacher.load_teachers()
    if request.method == 'POST':
        teacher = Teacher.get_teacher_by_id(teacher_id, teachers)
        if teacher:
            # 假设请求的数据格式是 {'schedule': [{'date': '...', 'time': '...', 'event': '...'}]}
            data = request.json
            if 'schedule' in teacher[0]:
                schedule_teacher=data.get('schedule')
                teacher[0]['schedule'].append(schedule_teacher[0]) 
                Teacher.save_teachers(teachers)
                return jsonify({"message": "Schedule updated successfully"}), 200
            else:
                teacher[0]['schedule'] = data.get('schedule')
                Teacher.save_teachers(teachers)
                return jsonify({"message": "Schedule updated successfully"}), 200
        else:
            return jsonify({"error": "Teacher not found"}), 404
    else:
        return render_template('schedule_update.html')
    
    

if __name__ == '__main__':
    app.run(debug=True)