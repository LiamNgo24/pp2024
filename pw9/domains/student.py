import numpy as np

class Student:
    def __init__(self, student_id, name, dob):
        self.__student_id = student_id
        self.__name = name
        self.__dob = dob
        self.__marks = {}

    def add_mark(self, course_id, mark):
        self.__marks[course_id] = mark

    # Getters
    def get_student_id(self):
        return self.__student_id

    def get_name(self):
        return self.__name

    def get_dob(self):
        return self.__dob

    def get_marks(self, course_id):
        return self.__marks.get(course_id, None)
    
    def calculate_gpa(self):
        if not self.__marks:
            return 0  # No marks available
        marks_array = np.array(list(self.__marks.values()))
        # Assuming GPA is the average mark on a scale of 0-20
        gpa = np.mean(marks_array)
        return gpa