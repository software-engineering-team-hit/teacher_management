from flask import Flask, request, jsonify,render_template
from model import Teacher

app = Flask(__name__,template_folder='F:\\2024_code\\software\\teacher_management\\templates')

# 初始化教师数据
teachers = Teacher.load_teachers()
print(teachers)
@app.route('/update_teacher', methods=['GET','POST'])
def update_teacher():
    if request.method == 'POST':
        id = request.form['id']
        print(id)
        print(type(id)) 
        name = request.form['name']
        academy = request.form['academy']
        url = request.form['url']

        # 找到要更新的教师对象
        for teacher in teachers:
            if str(teacher["id"]) == id:
                print("成功匹配")
                teacher["name"] = name
                teacher["academy"] = academy
                teacher["url"] = url
                break
            else:
                return jsonify({"error": "Teacher not found"}), 404

        # 保存更新后的教师数据
        Teacher.save_teachers(teachers)
        
        #return redirect(url_for('index'))
    
    return render_template('update.html')


if __name__ == '__main__':
    app.run()