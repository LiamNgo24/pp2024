import math
from unicodedata import name
from domains.student import Student
from domains.course import Course
from input import *
import os
import pickle
import gzip
import threading
import tkinter as tk

class ManagementSystem:
    def __init__(self):
        self.students = {}
        self.courses = {}
        self.lock = threading.Lock()
        self.load_data()


    def save_data(self):
        def save_data_thread():
            with gzip.open('./data/students.dat', 'wb') as file:
                data = {
                    'students': self.students,
                    'courses': self.courses,
                }
                pickle.dump(data, file)

        thread = threading.Thread(target=save_data_thread)
        thread.start()

    def load_data(self):
        if os.path.exists('./data/students.dat'):
            with gzip.open('./data/students.dat', 'rb') as file:
                data = pickle.load(file)
                self.students = data['students']
                self.courses = data['courses']


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
        print("9. Calculate and display student's GPA")
        print("10. List GPA of students (sorted descending)")
        print("0. Exit")
        choice = input("Enter your choice: ")
        print()
        return choice


    def input_student(self):
        number = get_integer_input("Enter the number of students: ")
        with open('./data/students.txt', 'a') as student_file:
            for _ in range(number):
                student_id = get_integer_input("Enter student's ID: ")
                name = get_non_numeric_input("Enter student's name: ")
                dob = get_valid_date("Enter student's date of birth (dd/mm/yyyy): ")
                self.students[student_id] = Student(student_id, name, dob)
                student_file.write(f"{student_id},{name},{dob}\n")
                self.save_data()

    def input_courses(self):
        number = get_integer_input("Enter the number of courses: ")
        with open('./data/courses.txt', 'a') as courses_file:
            for _ in range(number):
                course_id = get_integer_input("Enter course ID: ")
                name = get_non_numeric_input("Enter course name: ")
                self.courses[course_id] = Course(course_id, name)
                courses_file.write(f"{course_id},{name}\n")
                self.save_data()

    def input_marks(self):
        course_id = get_integer_input("Enter the course ID to input marks: ")
        if course_id not in self.courses:
            print("Course not found.")
            return
        course_name = self.courses[course_id].get_name()
        with open('./data/marks.txt', 'a') as marks_file:
            for student_id, student in self.students.items():
                mark = float(input(f"Enter mark for student {student_id} ({student.get_name()}): "))
                student.add_mark(course_id, math.floor(mark))
                marks_file.write(f"{student_id},{course_name},{mark}\n")
                self.save_data()


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

    def print_student_gpa(self):
        student_id = get_integer_input("Enter the student's ID to see GPA: ")
        if student_id in self.students:
            student = self.students[student_id]
            gpa = student.calculate_gpa()
            print(f"Student {student_id} ({student.get_name()}) has a GPA of: {gpa:.2f}")
        else:
            print("Student not found.")

    def sort_students_by_gpa(self):
            # Calculate GPA for all students and store in a list of tuples [(student_id, gpa), ...]
            students_with_gpa = [(student_id, student.calculate_gpa()) for student_id, student in self.students.items()]
            
            sorted_students_with_gpa = sorted(students_with_gpa, key=lambda x: x[1], reverse=True)
            
            print("Students sorted by GPA (descending):")
            for student_id, gpa in sorted_students_with_gpa:
                student = self.students[student_id]
                print(f"ID: {student_id}, Name: {student.get_name()}, GPA: {gpa:.2f}")


def main():
    system = ManagementSystem()
    while True:
        choice = system.menu()
        if choice == '1':
            system.input_student()
        elif choice == '2':
            system.input_student()
        elif choice == '3':
            system.input_courses()
        elif choice == '4':
            system.input_courses()
        elif choice == '5':
            system.input_marks()
        elif choice == '6':
            system.list_courses()
        elif choice == '7':
            system.list_students()
        elif choice == '8':
            course_id = get_integer_input("Enter course ID to show marks: ")
            system.show_marks(course_id)
        elif choice == '9':
            system.print_student_gpa()
        elif choice == '10':
            system.sort_students_by_gpa()
        elif choice == '0':
            print("Exiting the program ... \n")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
