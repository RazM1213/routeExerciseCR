import json


class Payload:
    def __init__(self, jsonBody):
        self.__dict__ = json.loads(jsonBody)
        self.studentDetails = None if "studentDetails" not in self.__dict__ else self.__dict__["studentDetails"]
        self.subjectGrades = None if "subjectGrades" not in self.__dict__ else self.__dict__["subjectGrades"]
        self.birthDate = None if "birthDate" not in self.__dict__ else self.__dict__["birthDate"]
        self.age = None if "age" not in self.__dict__ else self.__dict__["age"]
        self.gender = None if "gender" not in self.__dict__ else self.__dict__["gender"]
        self.behaviourGrade = None if "behaviourGrade" not in self.__dict__ else self.__dict__["behaviourGrade"]
        self.notes = None if "notes" not in self.__dict__ else self.__dict__["notes"]

