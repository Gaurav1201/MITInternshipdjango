from datetime import datetime
from django.db import connection
from .models import *
def courseDescriptionHelper(request_data):
    print("1111111111111111111111111111111111111111111111111111111111111111")
    print(request_data)
    #query to get all the data of that course
    query = """
    select 
    cs.course_code, cs.course_name, cs.course_description
    from tb_course cs
    where course_code = %s
   """
    current_year = datetime.now().year
        
     # Assuming academic year is calculated as current year + next year (i.e., 2024-2025 for current year 2024)
     #not used
    academic_year = int(str(current_year)[2:] + str(current_year + 1)[2:])  # e.g., 2425 for 2024
    with connection.cursor() as cursor:
       
        cursor.execute(query, [request_data['course_code']])
        rows = cursor.fetchall()
    #print(rows)
    #rows i tuple only has 1 row and 3 cols
    data = {
        'course_code': rows[0][0],
        'course_name': rows[0][1],
        'course_description': rows[0][2]
    }
    return data

def lessonPlanHelper(request_data):
    query="""
    select 
    lesson_id , descrption, co_num, course_code
    from 
    tb_lesson_plan
    where course_code = %s and academic_year = %s
    """
    
    with connection.cursor() as cursor:   
        cursor.execute(query, [request_data['course_code'], request_data['academic_year']])
        rows = cursor.fetchall()
    lesson_plan = []
    for row in rows:
        lesson_plan.append({
            
            'lesson_id': row[0],
            'description': row[1],
            'co_num': row[2],
            'course_code': row[3],
        })
    return {"lesson_plan":lesson_plan}

def courseOutcomesHelper(request_data):
    query="""
    select 
    co_num, description, contact_hours,marks, course_code
    from 
    tb_course_outcomes
    where course_code = %s 
    """
        
     # Assuming academic year is calculated as current year + next year (i.e., 2024-2025 for current year 2024)
     #not used
    current_year = datetime.now().year
    
    academic_year = int(str(current_year)[2:] + str(current_year + 1)[2:])  # e.g., 2425 for 2024
    
    with connection.cursor() as cursor:   
        cursor.execute(query, [request_data['course_code']])
        rows = cursor.fetchall()
    course_outcomes = []
    total_contact_hours = 0
    total_marks = 0
    for row in rows:
        
        course_outcomes.append({
            'co_num': row[0],
            'description': row[1],
            'contact_hour': row[2],
            'marks':int(row[3]),
            'course_code': row[4],            
        })
        total_contact_hours = total_contact_hours + row[2]
        total_marks = total_marks + int(row[3])
    print(course_outcomes)
    return {"course_outcomes":course_outcomes, "total_contact_hours":total_contact_hours, "total_marks":total_marks}