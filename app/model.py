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
            with open('E:\\csnerwork\\teacher_management\\TEACHERS_FILE.json', 'r', encoding='utf-8') as file:#绝对路径，相对路径好像有点问题
                teachers_data = json.load(file)
                return teachers_data
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_teachers(teachers):
        with open('E:\\csnerwork\\teacher_management\\TEACHERS_FILE.json', 'w',encoding='utf-8') as file:
            json.dump(teachers, file)

    @classmethod
    def get_teacher_by_id(cls, id, teachers_data):
        if id==" ":
            return teachers_data;
        teachers={teacher["id"]: teacher for teacher in teachers_data}
        for teacher in teachers_data:
            if teacher["id"]==id :
                teacher["times"]=str(int(teacher["times"])+1)
        with open('E:\\csnerwork\\teacher_management\\TEACHERS_FILE.json', 'w',encoding='utf-8') as file:
            json.dump(teachers_data, file)
        return [teachers.get(id)]

    @classmethod
    def get_teacher_by_email(cls, email, teachers_data):
        for teacher in teachers_data:
            if teacher['email']==email:
                return teacher


    @classmethod
    def get_teacher_by_name(cls, name, teachers_data):
        if name==" ":
            return teachers_data;
        teachers={}
        for teacher in teachers_data:
            if teacher["name"] ==name:
                teacher["times"] = str(int(teacher["times"])+1)
            tmp=teacher.get("name")
            if (teachers.get(tmp)!=None):
                newvalue=teachers[tmp]
                newvalue.append(teacher)
                print(newvalue)
                teachers[tmp]=newvalue
                #print(teachers[teacher["name"]])
            else:
                teachers[tmp]=[teacher]
        with open('E:\\csnerwork\\teacher_management\\TEACHERS_FILE.json', 'w',encoding='utf-8') as file:
            json.dump(teachers_data, file)
        return teachers.get(name)

    @classmethod
    def get_teacher_by_academy(cls, academy, teachers_data):
        if academy==" ":
            return teachers_data;
        else:
            teachers = {}
            for teacher in teachers_data:
                if teacher["academy"] == academy:
                    teacher["times"] = str(int(teacher["times"]) + 1)
                tmp = teacher.get("academy")
                if (teachers.get(tmp) != None):
                    newvalue = teachers[tmp]
                    newvalue.append(teacher)
                    # print(newvalue)
                    teachers[tmp] = newvalue
                    # print(teachers[teacher["name"]])
                else:
                    teachers[tmp] = [teacher]
            with open('E:\\csnerwork\\teacher_management\\TEACHERS_FILE.json', 'w', encoding='utf-8') as file:
                json.dump(teachers_data, file)
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
#teachers = Teacher.load_teachers()
#print(Teacher.get_teacher_by_academy("计算学部",teachers))
class Appointment:
    def __init__(self, student_name,student_email, academy, purpose, teacher_id, date, time, is_accepted=False):
        self.student_name = student_name
        self.student_email = student_email
        self.academy = academy
        self.purpose = purpose
        self.teacher_id = teacher_id
        self.date = date
        self.time = time
        self.is_accepted = is_accepted

    @staticmethod
    def load_appointments():
        try:
            with open("E:\\csnerwork\\teacher_management\\appointment.json", 'r', encoding='utf-8') as file:#绝对路径，相对路径好像有点问题
                appointments_data = json.load(file)
                return appointments_data
        except FileNotFoundError:
            return {}

    @staticmethod
    def save_appointment(appointment):
        with open("E:\\csnerwork\\teacher_management\\appointment.json", 'w', encoding='utf-8') as file:
            json.dump(appointment, file)

    @staticmethod
    def check_conflict(teacher_id, date, time):
        # 检查预约时间是否冲突
        appointments = Appointment.load_appointments()
        for app in appointments:
            if app.teacher_id == teacher_id and app.date == date and app.time == time:
                return True
        return False