import re
import math
import numpy
import curses

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

class Course:
    def __init__(self, course_id, name):
        self.__course_id = course_id
        self.__name = name

    # Getters
    def get_course_id(self):
        return self.__course_id

    def get_name(self):
        return self.__name

class ManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def menu(self):
        print("\n--- Student Mark Management System ---")
        print("1. Input number of students in a class")
        print("2. Input student information")
        print("3. Input number of courses")
        print("4. Input course information")
        print("5. Select a course and input marks for students")
        print("6. List courses")
        print("7. List students")
        print("8. Show student marks for a given course")
        print("9. Exit")
        choice = input("Enter your choice: ")
        print()
        return choice

    def input_student(self):
        number = self._get_integer_input("Enter the number of students: ")
        for _ in range(number):
            student_id = self._get_integer_input("Enter student's ID: ")
            name = self._get_non_numeric_input("Enter student's name: ")
            dob = self._get_valid_date("Enter student's date of birth (dd/mm/yyyy): ")
            self.students[student_id] = Student(student_id, name, dob)

    def input_courses(self):
        number = self._get_integer_input("Enter the number of courses: ")
        for _ in range(number):
            course_id = self._get_integer_input("Enter course ID: ")
            name = self._get_non_numeric_input("Enter course name: ")
            self.courses[course_id] = Course(course_id, name)

    def input_marks(self):
        course_id = self._get_integer_input("Enter the course ID to input marks: ")
        if course_id not in self.courses:
            print("Course not found.")
            return
        for student_id, student in self.students.items():
            mark = float(input(f"Enter mark for student {student_id} ({student.get_name()}): "))
            student.add_mark(course_id, math.floor(mark))

    def list_courses(self):
        if not self.courses:
            print("There are no courses. Input a course first.")
        else:
            for course_id, course in self.courses.items():
                print(f"Course ID: {course_id}, Name: {course.get_name()}")

    def list_students(self):
        if not self.students:
            print("There are no students. Input information of a student first.")
        else:
            for student_id, student in self.students.items():
                print(f"ID: {student_id}, Name: {student.get_name()}, DoB: {student.get_dob()}")

    def show_marks(self, course_id):
        if course_id not in self.courses:
            print("Course not found.")
            return
        print(f"Marks for course {self.courses[course_id].get_name()}:")
        for student_id, student in self.students.items():
            mark = student.get_marks(course_id)
            if mark is None:
                mark = "N/A"
            print(f"Student {student_id} ({student.get_name()}): {mark}")

    def _get_integer_input(self, prompt):
        while True:
            try:
                return int(input(prompt))
            except ValueError:
                print("This value must be an integer. Please try again.")

    def _get_non_numeric_input(self, prompt):
        while True:
            value = input(prompt)
            if not value.isnumeric():
                return value
            else:
                print("Value cannot be a number. Please try again.")

    def _get_valid_date(self, prompt):
        while True:
            value = input(prompt)
            if re.match(r'^\d{2}/\d{2}/\d{4}$', value):
                return value
            else:
                print("Invalid date format. Please use the format dd/mm/yyyy.")

def main():
    system = ManagementSystem()
    while True:
        choice = system.menu()
        if choice == '1' or choice == '2':
            system.input_student()
        elif choice == '3' or choice == '4':
            system.input_courses()
        elif choice == '5':
            system.input_marks()
        elif choice == '6':
            system.list_courses()
        elif choice == '7':
            system.list_students()
        elif choice == '8':
            course_id = system._get_integer_input("Enter course ID to show marks: ")
            system.show_marks(course_id)
        elif choice == '9':
            print("Exiting the program ... \n")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()