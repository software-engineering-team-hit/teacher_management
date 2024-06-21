from flask import Flask, render_template, request, jsonify
from app.model import Teacher


def create_app():
    app = Flask(__name__, template_folder='E:\\csnerwork\\teacher_management\\templates')

    @app.route('/')
    def index():
        # 渲染搜索页面
        return render_template('menu.html')
    @app.route('/search')
    def search():
        # 渲染搜索页面
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

    return app
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)
