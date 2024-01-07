import re

def menu():
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

# def input_student():
#     number = int(input("Enter the number of students: "))
#     for _ in range(number):
#         id = input("\nEnter student's ID: ")
#         name = input("Enter student's name: ")
#         dob = input("Enter student's date of birth (dd/mm/yyyy): ")
#         students[id] = {'name': name, 'DoB': dob, 'marks': {}}

def input_student():
    while True:
        try:
            number = int(input("Enter the number of students: "))
            break
        except ValueError:
                print("This value must be an integer. Please try again.")
    
    for _ in range(number):
        while True:
            try:
                id = int(input("\nEnter student's ID: "))
                break
            except ValueError:
                print("ID must be an integer. Please try again.")
        
        while True:
            name = input("Enter student's name: ")
            if not name.isnumeric():
                break
            else:
                print("Name cannot be a number. Please try again.")
        
        while True:
            dob = input("Enter student's date of birth (dd/mm/yyyy): ")
            if re.match(r'^\d{2}/\d{2}/\d{4}$', dob):
                break
            else:
                print("Invalid date format. Please use the format dd/mm/yyyy.")

        students[id] = {'name': name, 'DoB': dob, 'marks': {}}

def input_courses():
    number = int(input("Enter the number of courses: "))
    for _ in range(number):
        id = input("\nEnter course ID: ")
        name = input("Enter course name: ")
        courses[id] = name

def input_marks(course_id):
    if course_id not in courses:
        print("Course not found.")
        return
    for student_id in students:
        mark = float(input(f"Enter mark for student {student_id} ({students[student_id] ['name']}): "))
        students[student_id] ['marks'] [course_id] = mark

def list_courses():
    if len(courses) == 0:
        print("There are no courses. Input a course first.")
    else:
        for id, name in courses.items():
            print(f"{id}, {name}")
    

def list_students():
    if len(students) == 0:
        print("There are no students. Input information of a student first.")
    else: 
        for id, info in students.items():
            print(f"ID: {id}, Name: {info['name']}, DoB: {info['DoB']}")

def show_marks(course_id):
    if course_id not in courses:
        print("Course not found.")
        return
    print(f"Marks for course {courses[course_id]}:")
    for student_id, info in students.items():
        mark = info['marks'].get(course_id, "N/A")
        print(f"Student {student_id} ({info['name']}): {mark}")

def main():
    global students, courses
    students = {}
    courses = {}

    while True:
        choice = menu()
        if choice == '1':
            input_student()
        elif choice == '2':
            input_student()
        elif choice == '3':
            input_courses()
        elif choice == '4':
            input_courses()
        elif choice == '5':
            course_id = input("Enter the course ID to input marks: ")
            input_marks(course_id)
        elif choice == '6':
            list_courses()
        elif choice == '7':
            list_students()
        elif choice == '8':
            course_id = input("Enter course ID to list marks: ")
            show_marks(course_id)
        elif choice == '9':
            print("Exiting the program ... \n")
            break
        else:
            print("Invalid choice. Please try again.")

main()