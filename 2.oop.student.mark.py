# from msilib.schema import SelfReg
# from typing import Self
import re


class Student:
    def __init__(self, student_id, name, dob):
        self.student_id = student_id
        self.name = name
        self.dob = dob
        self.marks = {}

    def add_mark(self, course_id, mark):
        self.marks[course_id] = mark

class Course:
    def __init__(self, course_id, name):
        self.course_id = course_id
        self.name = name

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
        for student_id in self.students:
            mark = float(input(f"Enter mark for student {student_id} ({self.students[student_id].name}): "))
            self.students[student_id].add_mark(course_id, mark)

    def list_courses(self):
        if not self.courses:
            print("There are no courses. Input a course first.")
        else:
            for course in self.courses.values():
                print(f"{course.course_id}, {course.name}")

    def list_students(self):
        if not self.students:
            print("There are no students. Input information of a student first.")
        else:
            for student in self.students.values():
                print(f"ID: {student.student_id}, Name: {student.name}, DoB: {student.dob}")

    def show_marks(self, course_id):
        # course_id = self._get_integer_input("Enter course ID to list marks: ")
        if course_id not in self.courses:
            print("Course not found.")
            return
        print(f"Marks for course {self.courses[course_id].name}:")
        for student in self.students.values():
            mark = student.marks.get(course_id, "N/A")
            print(f"Student {student.student_id} ({student.name}): {mark}")

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