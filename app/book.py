from flask import Flask, request, jsonify, render_template
from model import Appointment
import json

app = Flask(__name__, template_folder='F:\\2024_code\\software\\teacher_management\\templates')

@app.route('/teacher/<int:teacher_id>/book', methods=['GET', 'POST'])
def book_teacher(teacher_id):
    if request.method == 'POST':
        data = request.json
        
        # 检查时间冲突的逻辑（已注释）
        # if Appointment.check_conflict(teacher_id, data.get('date'), data.get('time')):
        #     return jsonify({"error": "Time conflict, please choose another time"}), 409
        
        
        #构造字典
        appointment_dict = {
            'studentName': data.get('studentName'),
            'academy': data.get('academy'),
            'purpose': data.get('purpose'),
            'teacherId': teacher_id,
            'date': data.get('date'),
            'time': data.get('time'),
            'is_accepted' : False
        }
        print(appointment_dict)


        try:
            appointments=Appointment.load_appointments()
            appointments.append(appointment_dict)
        except json.decoder.JSONDecodeError:
            appointments=[]
            appointments.append(appointment_dict)

        


        Appointment.save_appointment(appointments)
        
        return jsonify({"message": "预约信息已经发给教师，等待确认", "appointment": appointment_dict}), 201

    else:
        return render_template('book.html')

if __name__ == '__main__':
    app.run(debug=True)