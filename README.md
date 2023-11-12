# SQL Database Query Application
### Introduction
In this project an application was created in Python to query an SQL dataset with data about students and teachers in a school, with details such as their email and home address, and which classes they attend or teach. The user can find information about someone based on their student ID, teacher ID or their name using the application.
### Getting Started
To run the code you will need to install Python on your device. Also ensure that you have SQLite installed on your system.
Ensure that the python file 'lookup.py' is in the same directory as the 'create_database.sql' file.

You will need to create an SQLite database file named "HyperionDev.db." 
To do this, run the following command in your terminal:
"sqlite3 HyperionDev.db"
This will create an empty database file.

Next, you need to execute the SQL script to create the tables and populate the database. 
You can do this by running the following command in your terminal:
".read create_database.sql"
You can check if it has worked by typing ".tables" into the terminal. It should print the following table names:
'Address', 'Review', 'StudentCourse', 'Course', 'Student', and 'Teacher'.

### Project Overview
Now the Python code 'lookup.py' can be run. You can view all the data values in the 'create_database.sql' file and use
some of them as inputs to query the database in the app. The main menu of the application is as shown below, where the user is asked to
indicate what they would like to do by typing the corresponding letters into the terminal:
```python
'''What would you like to do?

d - demo                   - lists all names in the dataset
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program'''
```
