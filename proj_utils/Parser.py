from time import sleep

from models.Payload import Payload
import os
import json


class Parser:
    def __init__(self, payload: Payload):
        self.payload = payload
        self.jsonObject = {}

    def create_text_file(self):
        save_path = 'C:/Users/razm1/PycharmProjects/routeExercise/students'
        fullname = f"{self.jsonObject['studentDetails']['fullName']}"
        complete_path = os.path.join(save_path, fullname.replace(' ', '_') + ".txt")

        with open(complete_path, 'w') as f:
            data = json.dumps(self.jsonObject, indent=4)
            f.write(data)

    def populate_json_object(self):
        self.populate_student_details()
        self.populate_subject_grades()
        self.populate_total_avg()
        self.populate_birth_date()
        self.populate_age()
        self.populate_gender()
        self.populate_isgoodbehavior()
        self.populate_notes()

    def populate_student_details(self):
        self.jsonObject["studentDetails"] = {}
        self.jsonObject["studentDetails"].update({
            "firstName": f"{self.payload.studentDetails['firstName']}",
            "lastName": f"{self.payload.studentDetails['lastName']}",
            "fullName": f"{self.payload.studentDetails['firstName']} {self.payload.studentDetails['lastName']}"
        })

    def populate_subject_grades(self):
        self.jsonObject["subjectGrades"] = []
        for subject in self.payload.subjectGrades:
            self.jsonObject["subjectGrades"].append({
                "subject": f"{subject['subject']}",
                "avg": f"{sum(subject['grades']) / len(subject['grades'])}"
            })

    def populate_total_avg(self):
        sum = 0
        for subject in self.jsonObject["subjectGrades"]:
            sum += float(subject["avg"])

        self.jsonObject["totalAvg"] = sum / len(self.jsonObject["subjectGrades"])

    def populate_birth_date(self):
        self.jsonObject["birthDate"] = self.payload.birthDate

    def populate_age(self):
        self.jsonObject["age"] = self.payload.age

    def populate_gender(self):
        if self.payload.gender == "זכר":
            self.jsonObject["gender"] = "MALE"
        elif self.payload.gender == "נקבה":
            self.jsonObject["gender"] = "FEMALE"
        elif self.payload.gender == "אחר":
            self.jsonObject["gender"] = "OTHER"

    def populate_isgoodbehavior(self):
        self.jsonObject["isGoodBehavior"] = "true" if self.payload.behaviourGrade > 5 else "false"

    def populate_notes(self):
        if self.payload.notes is not None:
            self.jsonObject["notes"] = self.payload.notes

