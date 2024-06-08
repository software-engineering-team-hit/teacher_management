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
            with open('F:\\2024_code\\software\\teacher_management\\TEACHERS_FILE.json', 'r', encoding='utf-8') as file:#绝对路径，相对路径好像有点问题
                teachers_data = json.load(file)
                return teachers_data
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_teachers(teachers):
        with open('F:\\2024_code\\software\\teacher_management\\TEACHERS_FILE.json', 'w',encoding='utf-8') as file:
            json.dump(teachers, file, indent=2,ensure_ascii=False)

    @classmethod
    def get_teacher_by_id(cls, id, teachers_data):
        teachers={teacher["id"]: teacher for teacher in teachers_data}
        return teachers.get(id)

    @classmethod
    def get_teacher_by_name(cls, name, teachers_data):
        teachers={}
        for teacher in teachers_data:
            tmp=teacher.get("name")
            if (teachers.get(tmp)!=None):
                newvalue=teachers[tmp]
                newvalue.append(teacher)
                print(newvalue)
                teachers[tmp]=newvalue
                #print(teachers[teacher["name"]])
            else:
                teachers[tmp]=[teacher]
        return teachers.get(name)

    # @classmethod
    # def get_teacher_by_academy(cls, academy, teachers_data):
    #     teachers={}
    #     for teacher in teachers_data:
    #         tmp= teacher.get("academy")
    #         if (teachers.get(tmp) != None):
    #             newvalue = teachers[tmp]
    #             newvalue.append(teacher)
    #             #print(newvalue)
    #             teachers[tmp] = newvalue
    #             # print(teachers[teacher["name"]])
    #         else:
    #             teachers[tmp] = [teacher]
    # 定义其他类方法，例如添加、更新、删除教师等..
teachers = Teacher.load_teachers()
