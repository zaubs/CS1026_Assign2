
"""
Zach Aubry
zaubry@uwo.ca
251307316
Computer Science 1026A
File Created on May 22nd, 2025

This file is for the second assignment in the course CS 1026A, and it goes through a given list of school courses and it finds important course names,
unique majors for provided course sections, average marks from students in a given course, if students enrolled have paid their tuition, if courses
have an exceeding amount of students and if any course timeslot passes through noon.

"""







# PLEASE DON'T CHANGE THIS FUNCTION
def pprint_schedule(schedule):
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(schedule)

# PLEASE DON'T CHANGE THIS FUNCTION
import pickle
def load_schedule(filename):
    with open(filename, 'rb') as file:
        schedule = pickle.load(file)
    return schedule

# Finds course names that contains the given keyword, and returns those course names in a list
def find_sections_by_course_name(schedule, keyword): 
    matching_sections = []
    for course in schedule: # To iterate through each course in the schedule
        course_no = course[0]
        course_name = course[1] 
        if keyword in course_name.lower(): # Executes if keyword is in the course name
            matching_sections.append(course_no) 

    return matching_sections

# Finds the courses enrolled by the student with the given student number, which are returned in a list
def find_courses_by_student_number(schedule, student_number): # Finds the courses enrolled by the student with the given student number, which are returned in a list
    enrolled_courses = []
    for course in schedule: 
        course_name = course[1] 
        student_info = course[6]
        for student in student_info: # iterates through student info list in each course
            student_no = student[0]
            if student_number == student_no: # Executes if given number matches any number enrolled in the course and adds course name if it does
                enrolled_courses.append(course_name)

    return enrolled_courses
    
# Calculates the average mark of the midterm, project, and exam from the provided course; all of which are returned in a tuple
def calculate_mark_averages_by_section(schedule, section_no): 
    midterm_mark_sum = 0.0 # These three lines for taking sum of each assessment grade
    project_mark_sum = 0.0
    exam_mark_sum = 0.0
    student_count = 0 # This line is to keep track of enrolled students
    for course in schedule:
        course_no = course[0]
        student_info = course[6]
        if section_no == course_no: # Executes if the given section number matches one in the initial list
            for student in student_info:
                midtrm_mark = student[5] 
                project_mark = student[6]
                exam_mark = student[7]

                midterm_mark_sum += float(midtrm_mark) 
                project_mark_sum += float(project_mark)
                exam_mark_sum += float(exam_mark)
                student_count += 1 # Adds to counter for enrolled students
                
            midterm_avg = midterm_mark_sum / student_count # Sum of marks divided by number of students enrolled
            project_avg = project_mark_sum / student_count
            exam_avg = exam_mark_sum / student_count

    return (round(midterm_avg, 2), round(project_avg, 2), round(exam_avg, 2)) 

# Checks if all students at the school had paid their tuition 
def get_paid_students(schedule): 
    paid_students = []
    for course in schedule:
        student_info = course[6]
        for student in student_info: 
            student_no = student[0] 
            paid_tuition = student[4] 
            if paid_tuition == True: # executes if tuition is paid by the student
                paid_students.append(student_no) 
            else:
                continue # Goes to next student if they have not paid yet

    return paid_students

# The unique majors from the provided course are collected and returned in a list
def get_unique_majors_from_one_section(schedule, section_no): 
    unique_majors = []  
    for course in schedule:
        course_no = course[0]
        student_info = course[6]
        if section_no == course_no:
            for student in student_info:
                student_major = student[2] 
                if student_major not in unique_majors: # Checks if the major is already in the list, and adds it if not
                    unique_majors.append(student_major)
                else:
                    continue

    return unique_majors

# The unique majors from the provided course list are collected and returned in a new list
def get_unique_majors(schedule, section_nos):
    unique_majors = []  
    for course in schedule:
        course_no = course[0]
        student_info = course[6]
        for section_no in section_nos: # Iterates through each provided course number
        
            if section_no == course_no:
                for student in student_info:
                    student_major = student[2]
                    if student_major not in unique_majors: 
                        unique_majors.append(student_major)
                    else:
                        continue # This works, but could have also been done by calling the previous function

    return unique_majors

# Collects courses that start before noon and end past noon, and returns a list of tuples conatining course number and corresponding timeslot
def get_sections_past_noon(schedule): 
    sections_past_noon = []
    for course in schedule:
        course_no = course[0]
        course_time = course[2]
        before_noon = course_time[6:8] # String reading starting time's period of day (AM or PM)
        after_noon = course_time[17:19] # String reading ending time's period of day
        if before_noon.strip() == 'AM' and after_noon.strip() == 'PM': # Checks if the time starts with AM and ends in PM; in which, the class passes through noon
            sections_past_noon.append((course_no, course_time)) 

    return sections_past_noon

# Checks the courses in the provided wings and returns the courses with an exceeding amount of students in a list, providing the amount of excess students enrolled in the course
def find_sections_exceeding_capacity(schedule, wings): 
    sections_exceeding_capacity = []
    student_count = 0
    for course in schedule:
        course_no = course[0]
        capacity = course[5] 
        student_info = course[6]
        course_wing = course[4][-1] # String reading the wing letter of each course
        if course_wing.strip() in wings: # Checks if wing letter is in the provided list of wing letters
            for student in student_info:
                student_count += 1 # counts the number of students enrolled in the course

            if student_count > capacity: # Executes if the number of enrolled students exceeds the class size
                sections_exceeding_capacity.append(f"{course_no} with {student_count - capacity} extra student(s)")

        student_count = 0 # To reset the student counter for each class

    return sections_exceeding_capacity


# Function calls below

def main():
    schedule = load_schedule('data.pkl')
    
    pprint_schedule(schedule)


    # HERE YOU CALL THE FUNCTIONS
    # You can uncomment the function calls below to test them
    # Remember to comment them again when you submit your code to Gradescope

    

    # keyword = "computer"  # Example keyword
    keyword = str(input())
    matching_courses = find_sections_by_course_name(schedule, keyword)
    print(f"Courses containing '{keyword}':",matching_courses)


    # student_number = 'C321883'  # Example student number
    student_number = str(input())
    enrolled_courses = find_courses_by_student_number(schedule, student_number)
    print(f"Courses enrolled by student with number '{student_number}':",enrolled_courses)


    # section_no = 'Dif591'  # Example section number
    section_no = str(input()).title()
    mark_averages = calculate_mark_averages_by_section(schedule, section_no)
    print("Mark averages:",mark_averages)


    paid_students = get_paid_students(schedule)
    print("Student numbers who paid their tuition:",paid_students)

    # section_no = 'Cal558'  # Example of section number
    section_no = str(input()).title()
    unique_majors = get_unique_majors_from_one_section(schedule, section_no) 
    print("Unique major names for students in specified section:",unique_majors) 

    # section_nos = ['Cal558', 'Sta647', 'Env807']  # Example list of section numbers
    section_nos = str(input()).title().split()
    unique_majors = get_unique_majors(schedule, section_nos)
    print("Unique major names for students in specified sections:",unique_majors)

    sections_past_noon = get_sections_past_noon(schedule)
    print("Sections with class times passing through noon:",sections_past_noon)

    # wings = ['A', 'B', 'C']  # Example list of room wings
    wings = str(input()).split()
    sections_exceeding_capacity = find_sections_exceeding_capacity(schedule, wings)
    print("Sections with enrolled students exceeding capacity:",sections_exceeding_capacity)


# PLEASE DON'T CHANGE THIS FUNCTION CALL
# PLEASE KEEP THE IF STATEMENT, REMOVING THIS IF STATEMENT WILL CAUSE YOUR CODE TO FAIL
if __name__ == "__main__":
    main()

