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
from tkinter import ttk

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


    def init_gui():
        window = tk.Tk()
        window.title("Student Information System")
        window.geometry("800x600")
        return window


    def setup_ui(window, system):
        # Tabs for different functionalities
        tab_control = ttk.Notebook(window)
        student_tab = ttk.Frame(tab_control)
        course_tab = ttk.Frame(tab_control)
        marks_tab = ttk.Frame(tab_control)
        tab_control.add(student_tab, text='Students')
        tab_control.add(course_tab, text='Courses')
        tab_control.add(marks_tab, text='Marks')
        tab_control.pack(expand=1, fill="both")
        

        # Student Tab: Organize with two frames, one for input, one for list
        input_frame = ttk.Frame(student_tab)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Student input fields in the input frame
        ttk.Label(input_frame, text="Enter student details below:").grid(row=0, columnspan=2)

        ttk.Label(input_frame, text="ID:").grid(row=1, column=0, sticky=tk.W, padx=5)
        student_id_entry = ttk.Entry(input_frame)
        student_id_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        
        ttk.Label(input_frame, text="Name:").grid(row=2, column=0, sticky=tk.W, padx=5)
        student_name_entry = ttk.Entry(input_frame)
        student_name_entry.grid(row=2, column=1, sticky=tk.EW, padx=5)
        
        ttk.Label(input_frame, text="DoB:").grid(row=3, column=0, sticky=tk.W, padx=5)
        student_dob_entry = ttk.Entry(input_frame)
        student_dob_entry.grid(row=3, column=1, sticky=tk.EW, padx=5)
        
        # Make the entry widgets expand with the window
        input_frame.columnconfigure(1, weight=1)
        
        # List Frame
        list_frame = ttk.Frame(student_tab)
        list_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(list_frame, text="Student List").pack(side=tk.TOP, fill=tk.X)
        student_listbox = tk.Listbox(list_frame)
        student_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=student_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        student_listbox.config(yscrollcommand=scrollbar.set)
        
        for student_id, student in system.students.items():
            student_listbox.insert(tk.END, f"ID: {student_id}, Name: {student.get_name()}, DoB: {student.get_dob()}")
        
        # Function to move focus to next field
        def focus_next_widget(event):
            event.widget.tk_focusNext().focus()
            return("break")

        # Function to add a student to the system and list
        def add_student():
            # Retrieve the input data
            student_id = student_id_entry.get()
            name = student_name_entry.get()
            dob = student_dob_entry.get()

            # Simple validation
            if student_id and name and dob:
                system.students[student_id] = Student(student_id, name, dob)
                student_listbox.insert(tk.END, f"ID: {student_id}, Name: {name}, DoB: {dob}")

                system.save_data()

                # Clear the entry fields
                student_id_entry.delete(0, tk.END)
                student_name_entry.delete(0, tk.END)
                student_dob_entry.delete(0, tk.END)

                # Focus back to the first field
                student_id_entry.focus_set()

        # Bind the Return key to focus to next widget or add student
        student_id_entry.bind("<Return>", focus_next_widget)
        student_name_entry.bind("<Return>", focus_next_widget)
        student_dob_entry.bind("<Return>", lambda event: add_student())

        # Add button to add student
        add_button = ttk.Button(input_frame, text="Add Student", command=add_student)
        add_button.grid(row=4, columnspan=2, pady=5)


        # # Course Tab
        # ttk.Label(course_tab, text="Course List").pack()
        # course_listbox = tk.Listbox(course_tab)
        # course_listbox.pack(fill=tk.BOTH, expand=True)
        

        # Course Tab: Organize with two frames, one for input, one for list
        course_input_frame = ttk.Frame(course_tab)
        course_input_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Course input fields in the input frame
        ttk.Label(course_input_frame, text="Enter course details below:").grid(row=0, columnspan=2)

        ttk.Label(course_input_frame, text="Course ID:").grid(row=1, column=0, sticky=tk.W, padx=5)
        course_id_entry = ttk.Entry(course_input_frame)
        course_id_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        
        ttk.Label(course_input_frame, text="Course Name:").grid(row=2, column=0, sticky=tk.W, padx=5)
        course_name_entry = ttk.Entry(course_input_frame)
        course_name_entry.grid(row=2, column=1, sticky=tk.EW, padx=5)
        
        # Make the entry widgets expand with the window
        course_input_frame.columnconfigure(1, weight=1)
        
        # List Frame for courses
        course_list_frame = ttk.Frame(course_tab)
        course_list_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        ttk.Label(course_list_frame, text="Course List").pack(side=tk.TOP, fill=tk.X)
        course_listbox = tk.Listbox(course_list_frame)
        course_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        course_scrollbar = ttk.Scrollbar(course_list_frame, orient='vertical', command=course_listbox.yview)
        course_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        course_listbox.config(yscrollcommand=course_scrollbar.set)
        
        for course_id, course in system.courses.items():
            course_listbox.insert(tk.END, f"ID: {course_id}, Name: {course.get_name()}")

        # Function to add a course to the system and list
        def add_course():
            # Retrieve the input data
            course_id = course_id_entry.get()
            course_name = course_name_entry.get()

            # Simple validation
            if course_id and course_name:
                # Assuming course_id should be an integer
                try:
                    course_id_int = int(course_id)
                    system.courses[course_id_int] = Course(course_id_int, course_name)
                    course_listbox.insert(tk.END, f"ID: {course_id}, Name: {course_name}")
                    
                    # Save the data using the system's method
                    system.save_data()
                    
                    # Clear the entry fields
                    course_id_entry.delete(0, tk.END)
                    course_name_entry.delete(0, tk.END)
                    
                    # Focus back to the first field
                    course_id_entry.focus_set()
                except ValueError:
                    print("Please enter a valid integer for the Course ID.")

        course_id_entry.bind("<Return>", focus_next_widget)
        course_name_entry.bind("<Return>", lambda event: add_course())
        
        # Add button to add course
        add_course_button = ttk.Button(course_input_frame, text="Add Course", command=add_course)
        add_course_button.grid(row=3, columnspan=2, pady=5)


    window = init_gui()
    setup_ui(window, system)
    window.mainloop()


if __name__ == "__main__":
    main()
