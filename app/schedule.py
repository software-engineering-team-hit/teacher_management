from flask import Flask,  jsonify ,render_template
from model import Teacher  # 确保已经导入了修改后的Teacher类

app = Flask(__name__,template_folder='F:\\2024_code\\software\\teacher_management\\templates')

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
    


if __name__ == '__main__':
    app.run(debug=True)