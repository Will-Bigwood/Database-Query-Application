import sqlite3
import json
import xml.etree.ElementTree as ET

try:
    # Connect to the database
    conn = sqlite3.connect("HyperionDev.db")
except sqlite3.Error:
    print("Please store your database as HyperionDev.db")
    quit()

# Create a cursor object
cur = conn.cursor()

# Check if the users input has the correct number of arguments
def usage_is_incorrect(input, num_args):
    if len(input) != num_args + 1:
        print(f"The {input[0]} command requires {num_args} arguments.")
        return True
    return False

def store_data_as_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    pass

def store_data_as_xml(data, filename):
    root = ET.Element("data")
    for item in data:
        for key, value in item.items():
            element = ET.Element(key)
            element.text = str(value)
            root.append(element)

    tree = ET.ElementTree(root)
    tree.write(filename, encoding='utf-8', xml_declaration=True)
    pass

def offer_to_store(data):
    while True:
        print("Would you like to store this result?")
        choice = input("Y/[N]? : ").strip().lower()

        if choice == "y":
            filename = input("Specify filename. Must end in .xml or .json: ")
            ext = filename.split(".")[-1]
            if ext == 'xml':
                store_data_as_xml(data, filename)
                break
            elif ext == 'json':
                store_data_as_json(data, filename)
                break
            else:
                print("Invalid file extension. Please use .xml or .json")

        elif choice == 'n':
            break

        else:
            print("Invalid choice")

usage = '''
What would you like to do?

d - demo                   - lists all names in the dataset
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("Welcome to the data querying app!")

while True:
    
    # Get input from user
    print()
    user_input = input(usage).split(" ")
    print()

    # Parse user input into command and args
    command = user_input[0]
    if len(user_input) > 1:
        args = user_input[1:]

    if command == 'd': # Print all the names and surnames
        print('People in the database:')
        data = cur.execute("SELECT * FROM Student")
        for _, firstname, surname, _, _ in data:
            print(f"{firstname} {surname}")
        
    elif command == 'vs': # view subjects by student_id
        if usage_is_incorrect(user_input, 1):
            continue      
        student_id = args[0]
        file_data = []
        
        # Create a list of student ids from the database
        student_id_data = cur.execute('''SELECT student_id FROM Student''')
        student_ids_list = [str(id[0]) for id in student_id_data]


        # Check if the Student ID entered is not in the list of student IDs, print error message.
        if student_id not in student_ids_list:
            print("There are no IDs that match your input.\n")
        
        # If ID check passed, fetch course_name data from database using student_id
        else:
            data = cur.execute('''SELECT Course.course_name 
                            FROM Course INNER JOIN StudentCourse
                            ON Course.course_code = StudentCourse.course_code 
                            WHERE StudentCourse.student_id =?''', (student_id,))
            
            # Print each course to the console and append the data to the file_data list in a dictionary format
            for course in data.fetchall():
                print(course[0])
                print()
                file_data.append({student_id : course[0]})
            
            offer_to_store(file_data)
            pass

    elif command == 'la':# list address by name and surname
        if usage_is_incorrect(user_input, 2):
            continue
        firstname, surname = args[0], args[1]
        full_name = f"{firstname}_{surname}"
        file_data = []      
        
        # Create a list of student names from the database
        name_data = cur.execute('''SELECT first_name, last_name FROM Student''')
        names = [f"{name1}_{name2}" for name1, name2 in name_data]

        # Check if the name entered is in the list of student names
        if full_name not in names:
            print("There are no names that match your input.\n")
        
        # If name check passed, fetch address data from database using the student name
        else:
            data = cur.execute('''SELECT Address.street, Address.city 
                            FROM Address INNER JOIN Student
                            ON Address.address_id = Student.address_id 
                            WHERE Student.first_name =? and Student.last_name=?''', (firstname,surname))
            
            # Print the address and append the data to the file_data list in a dictionary format
            for streetname,cityname in data.fetchall():  
                address = f"{streetname}, {cityname}"
                print(address)
                print()
                file_data.append({full_name : address})
            
            offer_to_store(file_data)
            pass
    
    elif command == 'lr':# list reviews by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        file_data = []
        
        # Create a list of student ids from the database
        student_id_data = cur.execute('''SELECT student_id FROM Student''')
        student_ids_list = [str(id[0]) for id in student_id_data]


        # Check if the Student ID entered is not in the list of student IDs, print error message.
        if student_id not in student_ids_list:
            print("There are no IDs that match your input.\n")

        # If ID check passed, fetch review data from database using the student ID
        else:
            data = cur.execute('''SELECT Review.completeness, Review.efficiency, Review.style, Review.documentation, Review.review_text 
                            FROM Review INNER JOIN Student
                            ON Review.student_id = Student.student_id 
                            WHERE Student.student_id=?''', (student_id,))
            number_of_reviews = 0
            for completeness,efficiency,style,documentation,review_text in data:
                number_of_reviews+=1
                format_review = f"{number_of_reviews}, {completeness}, {efficiency}, {documentation}, {review_text}"
                print(f'''Review number {number_of_reviews}:
                    
    Completeness:   {completeness}
    Efficiency:     {efficiency}
    Style:          {style}
    Documentation:  {documentation}
    Review:         {review_text}\n''')
                file_data.append({student_id : format_review})
                
            offer_to_store(file_data)
            pass

    elif command == 'lc': # List all courses being given by a specific teacher (search by teacher_id)
        if usage_is_incorrect(user_input, 1):
            continue
        teacher_id = args[0]
        file_data = []
        
        # Create a list of teacher IDs from the database
        teacher_id_data = cur.execute('''SELECT teacher_id FROM Teacher''')
        teacher_ids = [id[0] for id in teacher_id_data]

        # Check if the ID entered is in the list of teacher IDs
        if teacher_id not in teacher_ids:
            print("There are no IDs that match your input.\n")

        # If ID check passed, fetch course_name data from database using teacher_id
        else:
            data = cur.execute('''SELECT course_name FROM Course
                            WHERE teacher_id=?''', (teacher_id,))
            for course in data:
                print(course[0])
                print()
                file_data.append({teacher_id : course[0]})

            offer_to_store(file_data)
            pass
    
    elif command == 'lnc':# list all students who haven't completed their course
        file_data = []


        data = cur.execute('''SELECT Student.student_id, Student.first_name, Student.last_name,
                           Student.email, Course.course_name
                           FROM StudentCourse
                           INNER JOIN Student ON StudentCourse.student_id = Student.student_id
                           INNER JOIN Course ON StudentCourse.course_code = Course.course_code
                           WHERE StudentCourse.is_complete=?''', (0,))
        
        for student_id,firstname,lastname,email,coursename in data:
            format_student = f'''ID number: {student_id}
Name: {firstname} {lastname}
Email: {email}
Course: {coursename}\n'''
            print(format_student)
            file_data.append({"Course not completed" : format_student})

        offer_to_store(file_data)
        pass
    
    elif command == 'lf':# list all students who have completed their course and got a mark <= 30
        file_data = []
        
        data = cur.execute('''SELECT Student.student_id, Student.first_name, Student.last_name, Student.email, Course.course_name,
                           StudentCourse.mark FROM StudentCourse
                           INNER JOIN Student ON StudentCourse.student_id = Student.student_id
                           INNER JOIN Course ON StudentCourse.course_code = Course.course_code
                           WHERE StudentCourse.is_complete =? and StudentCourse.mark<=?''', (1,30))
        for student_id,firstname,lastname,email,coursename,mark in data:
            format_student = f'''ID number:  {student_id}
Name:       {firstname} {lastname}
Email:      {email}
Course:     {coursename}
Mark:       {mark}\n'''
            print(format_student)
            file_data.append({"Completed_course_and_failed" : format_student})

        offer_to_store(file_data)
        pass
    
    elif command == 'e':# Exit program
        print("Programme exited successfully!")
        break
    
    else:
        print(f"Incorrect command: '{command}'")
    

    
