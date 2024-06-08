import json
from flask import current_app

class Teacher:
    def __init__(self, id, name,academy, url, **kwargs):
        self.id = id
        self.name = name
        self.academy = academy
        self.url = url
        self.info = kwargs

    @staticmethod
    def load_teachers():
        try:
            with open('E:\\计网\\软件工程lab2\\TEACHERS_FILE.json', 'r', encoding='utf-8') as file:#绝对路径，相对路径好像有点问题
                teachers_data = json.load(file)
                return teachers_data
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_teachers(teachers):
        with open('E:\\计网\\软件工程lab2\\TEACHERS_FILE.json', 'w') as file:
            json.dump(list(teachers.values()), file)

    @classmethod
    def get_teacher_by_id(cls, id, teachers_data):
        teachers={teacher["id"]: teacher for teacher in teachers_data}
        return teachers.get(id)

    @classmethod
    def get_teacher_by_name(cls, name, teachers_data):
        teachers={}
        for teacher in teachers_data:
            if (teachers.get(teacher["name"])!=None):
                newvalue=teachers[teacher["name"]]
                newvalue.append(teacher)
                print(newvalue)
                teachers[teacher["name"]]=newvalue
                #print(teachers[teacher["name"]])
            else:
                teachers[teacher["name"]]=[teacher]
        return teachers.get(name)

    @classmethod
    def get_teacher_by_academy(cls, academy, teachers_data):
        teachers={}
        for teacher in teachers_data:
            if (teachers.get(teacher["academy"])!=None):
                newvalue=teachers[teacher["academy"]]
                newvalue.append(teacher)
                print(newvalue)
                teachers[teacher["academy"]]=newvalue
                #print(teachers[teacher["name"]])
            else:
                teachers[teacher["academy"]]=[teacher]
        return teachers.get(academy)

    @classmethod
    def update_information_of_teacher(cls, id, teacher_data):
        teacher = None
        for i in teacher_data:
            if (i["id"] == id):
                teacher = i
                break
        if (teacher == None):
            assert 0
        teacher.name = input("id:").strip()
        teacher.academy = input("academy:").strip()
        teacher.url = input("url:").strip()
        teacher.info = input("info:").strip()
        return


    # 定义其他类方法，例如添加、更新、删除教师等..
teachers = Teacher.load_teachers()