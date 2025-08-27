import sqlite3
import xml.etree.ElementTree as ET
import json as json



# Connecting to the database HyperionDev.db
try:
    conn = sqlite3.connect("HyperionDev.db")
except sqlite3.Error:
    # Quit if name of DB created does not match 
    print("Please store your database as HyperionDev.db")
    quit()

# Create cursor for executing sql commands
cur = conn.cursor()

def print_result(data):
    """Print results for variable length queries"""
    for record in data:
        print()
        for i in range(len(record)):
            print(record[i], end=" | ")    
        

def usage_is_incorrect(input, num_args):
    """
    Checks the number of words separated by a space and if it does not
    match the required input returns True, meaning the usage is incorrect
    """
    if len(input) != num_args + 1:
        print(f"""The {input[0]} command requires {num_args} arguments.
Enter command followed by required indentifer:
<student_id>
<teacher_id>
<firstname> <surname>""")
        return True
    return False


def get_header(data):
    """Returns a list of field names for use in export"""
    header_list = [description[0] for description in data.description]
    return header_list


def store_data_as_json(data, filename):
    """
    Takes user input and saves data into a JSON file
    """
    try:
        # Saving the data into a format that json library can use
        json_data = [dict(zip(headers, row)) for row in data]
        
        with open(filename, 'w') as outfile:
            json.dump(json_data, outfile, indent=4)

        print(f"Data successfully exported to {filename}")
        return True
        
    except Exception as e:
        print(f"An error occurred while saving data to JSON: {e}")
        return False
        

def store_data_as_xml(data, filename):
    """
    Takes user input and saves data into an XML file
    """
    try:
        # The root of the tree is called Requested data
        root = ET.Element("Lines")

        # For each row in data make a subelement called a record
        for row in data:
            record = ET.SubElement(root, "Record")
            # In Each record make a subelement named after each field
            # with the text contained in each row being the text stored
            # within that subelement
            for col, values in zip(headers, row):

                field = ET.SubElement(record, col)
                field.text = str(values)

        # Creating a tree object beginning with root (Records)
        tree = ET.ElementTree(root)

        # Opening a file and writing XML output to it
        with open(filename, 'wb') as outfile:
            tree.write(outfile, encoding='utf-8', xml_declaration=True)

        # Printing confirmation message
        print(f"Data successfully recorded to {filename}")  
        # Returning true to end outer loop
        return True
    
    except IOError as e:
        # Printing error message
        print(f"An error occured when trying to create {filename}: {e}")  
        # Continuing outer loop
        return False


def offer_to_store(data):
    """
    Executes a loop that breaks upon selecting n. it parses the filename
    input to decide whether to run the store_data function as XML or JSON
    """
    while True:
        print("Would you like to store this result?")
        choice = input("Y/[N]? : ").strip().lower()

        if choice == "y":
            filename = input("Specify filename. Must end in .xml or .json: ")
            ext = filename.split(".")[-1]
            output_success = False
            if ext == 'xml':
                output_success = store_data_as_xml(data, filename)
                if output_success == True:
                    break
            elif ext == 'json':
                output_success = store_data_as_json(data, filename)
                if output_success == True:
                    break
            else:
                print("Invalid file extension. Please use .xml or .json")

        elif choice == 'n':
            break

        else:
            print("Invalid choice")

# Initialising a menu
usage = '''
What would you like to do?

d - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("Welcome to the data querying app!")

# Menu loop
while True:
    print()
    # Get input from user
    user_input = input(usage).split(" ")
    print()

    # Parse user input into command and args
    command = user_input[0]
    if len(user_input) > 1:
        args = user_input[1:]

    if command == 'd': # demo - a nice bit of code from me to you - this prints all student names and surnames :)
        data = cur.execute("SELECT * FROM Student")
        for _, firstname, surname, _, _ in data:
            print(f"{firstname} {surname}")
        
    elif command == 'vs': # view subjects by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0] # Storing entered ID as a string

        # Saving the data retrieved from command into data variable
        data = cur.execute('''SELECT Course.course_name
FROM Course 
INNER JOIN StudentCourse ON Course.course_code = StudentCourse.course_code
INNER JOIN Student ON StudentCourse.student_id = Student.student_id
WHERE Student.student_id = ? ''', (student_id,))
        
        # Saving field names for use in outfile
        headers = get_header(data) 

        # Preserving data before pointer moves along
        data = cur.fetchall() 

        # Print to screen results of Select command
        print_result(data)
        
        # Offering to store data as xml or JSON
        offer_to_store(data)
        
    elif command == 'la':# list address by name and surname
        if usage_is_incorrect(user_input, 2):
            continue
        firstname, surname = args[0], args[1]
        data = cur.execute('''SELECT Address.street, Address.city
FROM Address 
INNER JOIN Student ON Address.address_id = Student.address_id
WHERE Student.first_name = ?
AND Student.last_name = ? ''', (firstname, surname))

        headers = get_header(data)

        data = cur.fetchall()

        print_result(data)
                
        offer_to_store(data)
        
    elif command == 'lr':# list reviews by student_id
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        data = cur.execute('''SELECT Review.completeness, 
                           Review.efficiency, Review.style, 
Review.documentation, Review.review_text
FROM Review
INNER JOIN StudentCourse ON StudentCourse.student_id = Review.student_id
                        AND StudentCourse.course_code = Review.course_code
WHERE Review.student_id = ?;''', (student_id,))
        
        headers = get_header(data)

        data = cur.fetchall()

        print_result(data)

        offer_to_store(data)
        
    elif command == 'lc':# List all courses taught by teacher
        if usage_is_incorrect(user_input, 1):
            continue
        teacher_id = args[0]
        data = cur.execute('''SELECT Course.course_name
FROM Course
INNER JOIN Teacher ON Teacher.teacher_id = Course.teacher_id
WHERE Course.teacher_id = ?''', (teacher_id,))

        headers = get_header(data)

        data = cur.fetchall()

        print_result(data)

        offer_to_store(data)

    elif command == 'lnc':# List all students who haven't completed their course
        data = cur.execute('''SELECT Student.student_id, 
Student.first_name, Student.last_name, Student.email, Course.course_name
FROM Student
INNER JOIN StudentCourse ON Student.student_id = StudentCourse.student_id
INNER JOIN Course ON StudentCourse.course_code = Course.course_code
WHERE StudentCourse.is_complete = 0;''')

        headers = get_header(data)

        data = cur.fetchall()

        print_result(data)
                
        offer_to_store(data)
        
    elif command == 'lf':# List all students who have completed their course and got a mark <= 30
        data = cur.execute('''SELECT Student.student_id, 
                           Student.first_name, Student.last_name, 
                           Student.email, Course.course_name,
                           StudentCourse.mark
FROM Student
INNER JOIN StudentCourse ON Student.student_id = StudentCourse.student_id
INNER JOIN Course ON StudentCourse.course_code = Course.course_code
WHERE StudentCourse.mark < 31 AND StudentCourse.is_complete = 1;''')

        headers = get_header(data)
        
        data = cur.fetchall()

        print_result(data)
        
        offer_to_store(data)
        
    elif command == 'e':# Exit program
        print("Programme exited successfully!")
        
        break
    
    else:
        print(f"Incorrect command: '{command}'")

# Close the database
conn.close()