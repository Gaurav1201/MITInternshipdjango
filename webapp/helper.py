from datetime import datetime
from django.db import connection
from .models import *
def courseDescriptionHelper(course_code):
    
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
       
        cursor.execute(query, [course_code])
        rows = cursor.fetchall()
    #print(rows)
    #rows i tuple only has 1 row and 3 cols
    data = {
        'course_code': rows[0][0],
        'course_name': rows[0][1],
        'course_description': rows[0][2]
    }
    return data

def lessonPlanHelper(course_code, academic_year):
    query="""
    select 
    lesson_id , description, co_num, course_code
    from 
    tb_lesson_plan
    where course_code = %s and academic_year = %s
    """
    
    with connection.cursor() as cursor:   
        cursor.execute(query, [course_code, academic_year])
        rows = cursor.fetchall()
    lesson_plan = []
    for row in rows:
        lesson_plan.append({
            
            'lesson_id': row[0],
            'description': row[1],
            'co_num': row[2],
            'course_code': row[3],
        })
    return lesson_plan