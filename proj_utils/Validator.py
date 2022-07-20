import datetime
import json
from jsonschema.validators import Draft3Validator


class Validator:
    schema = {
      "type": "object",
      "properties": {
        "studentDetails": {
          "type": "object",
          "properties": {
            "firstName": {
              "type": "string"
            },
            "lastName": {
              "type": "string"
            },
            "id": {
              "type": "integer"
            }
          },
          "required": [
            "firstName",
            "lastName",
            "id"
          ]
        },
        "subjectGrades": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "subject": {
                  "type": "string"
                },
                "grades": {
                  "type": "array",
                  "items": [
                    {
                      "type": "integer"
                    },
                    {
                      "type": "integer"
                    },
                    {
                      "type": "integer"
                    }
                  ]
                }
              },
              "required": [
                "subject",
                "grades"
              ]
            },
            {
              "type": "object",
              "properties": {
                "subject": {
                  "type": "string"
                },
                "grades": {
                  "type": "array",
                  "items": [
                    {
                      "type": "integer"
                    },
                    {
                      "type": "integer"
                    },
                    {
                      "type": "integer"
                    }
                  ]
                }
              },
              "required": [
                "subject",
                "grades"
              ]
            }
          ]
        },
        "birthDate": {
          "type": "string"
        },
        "age": {
          "type": "integer"
        },
        "gender": {
          "type": "string"
        },
        "behaviorGrade": {
          "type": "integer"
        },
        "notes": {
          "type": "string"
        }
      },
      "required": [
        "studentDetails",
        "subjectGrades",
        "birthDate",
        "age",
        "gender",
        "behaviorGrade",
        "notes"
      ]
    }

    def __init__(self, body):
        self.json_file = json.loads(body)
        self.message = ""
        self.is_valid_schema = Draft3Validator(Validator.schema).is_valid(self.json_file)

    def is_valid_firstname(self, firstName):
        if not firstName.isalpha():
            self.message += "Invalid First Name !\n"
            return False
        return True

    def is_valid_lastname(self, lastName):
        if any(char.isdigit() for char in lastName):
            self.message += "Invalid Last Name !\n"
            return False
        return True

    def is_valid_id(self, id):
        if len(str(id)) != 9 or not str(id).isnumeric():
            self.message += "Invalid id !\n"
            return False
        return True

    def is_valid_birthdate(self, birthDate):
        try:
            datetime.datetime.strptime(str(birthDate), '%d/%m/%Y')
        except ValueError:
            self.message += "Invalid birth date !\n"
            return False
        return True

    def is_valid_age(self, age, birthDate):
        if (datetime.datetime.now() - datetime.datetime.strptime(birthDate, "%d/%m/%Y")).days // 365 != age:
            self.message += "Invalid age !\n"
            return False
        return True

    def is_valid_gender(self, gender):
        if gender not in ["נקבה", "אחר", "זכר"]:
            self.message += "Invalid gender !\n"
            return False
        return True

    def is_valid_behaviour_grade(self, behaviourGrade):
        if behaviourGrade not in [i for i in range(1, 11)]:
            self.message += "Invalid behaviour grade !\n"
            return False
        return True

    def are_grades_valid(self, subjects):
        for subject in subjects:
            for grade in subject['grades']:
                if not 0 <= float(grade) <= 100:
                    self.message += "Invalid grade !\n"
                    return False
        return True

    def is_valid_values(self, json_body):
        validated_fields = []
        validated_fields.append(self.is_valid_firstname(json_body["studentDetails"]["firstName"]))
        validated_fields.append(self.is_valid_lastname(json_body["studentDetails"]["lastName"]))
        validated_fields.append(self.is_valid_id(json_body["studentDetails"]["id"]))
        validated_fields.append(self.is_valid_birthdate(json_body["birthDate"]))
        if validated_fields[3]:
            validated_fields.append(self.is_valid_age(json_body["age"], json_body["birthDate"]))
        validated_fields.append(self.is_valid_gender(json_body["gender"]))
        validated_fields.append(self.is_valid_behaviour_grade(json_body["behaviourGrade"]))
        validated_fields.append(self.are_grades_valid(json_body["subjectGrades"]))
        if False in validated_fields:
            print(self.message)
            return False

        return True

    def is_valid_fields(self):
        for field in ["studentDetails", "subjectGrades", "birthDate", "age", "gender", "behaviourGrade"]:
            if field not in self.json_file:
                return False

        for sub_field in ["firstName", "lastName", "id"]:
            if sub_field not in self.json_file["studentDetails"]:
                return False

        for i in range(len(self.json_file["subjectGrades"])):
            for sub_field in ["subject", "grades"]:
                if sub_field not in self.json_file["subjectGrades"][i]:
                    return False

        return True
