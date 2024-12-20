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

def assesementPlanHelper(request_data):
    query="""
    select 
    component, mid_sem_exam,flexible_assessments,end_semester_exam
    from 
    tb_AssesmentPlan
    where course_code = %s 
    """
        
     # Assuming academic year is calculated as current year + next year (i.e., 2024-2025 for current year 2024)
     #not used
    current_year = datetime.now().year
    
    academic_year = int(str(current_year)[2:] + str(current_year + 1)[2:])  # e.g., 2425 for 2024
    
    with connection.cursor() as cursor:   
        cursor.execute(query, [request_data['course_code']])
        rows = cursor.fetchall()
    a_plan = []
   
    for row in rows:
        
        a_plan.append({
            'component': row[0],
            'mid_sem_exam': row[1],
            'flexible_asssement': row[2],
            'end_semester_exam':row[3],
                      
        })
       
    print(a_plan)
    return {"a_plan":a_plan}


def referencesHelper(request_data):
    slno = 1
    query="""
    select 
    course_reference
    from 
    tb_course
    where course_code = %s 
    """
        
     # Assuming academic year is calculated as current year + next year (i.e., 2024-2025 for current year 2024)
     #not used
    current_year = datetime.now().year
    
    academic_year = int(str(current_year)[2:] + str(current_year + 1)[2:])  # e.g., 2425 for 2024
    
    with connection.cursor() as cursor:   
        cursor.execute(query, [request_data['course_code']])
        rows = cursor.fetchall()
    
    dataObject = []
    cr = rows[0][0].split("@!")
    print(cr)
    for row in cr:
        
        dataObject.append({
            'slno': slno,
            'reference': row,          
        })
        slno = slno + 1
       
    print(cr)
    return {"dataObject":dataObject}


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

def assesementPlanHelper(request_data):
    query="""
    select 
    component, mid_sem_exam,flexible_assessments,end_semester_exam
    from 
    tb_AssesmentPlan
    where course_code = %s 
    """
        
     # Assuming academic year is calculated as current year + next year (i.e., 2024-2025 for current year 2024)
     #not used
    current_year = datetime.now().year
    
    academic_year = int(str(current_year)[2:] + str(current_year + 1)[2:])  # e.g., 2425 for 2024
    
    with connection.cursor() as cursor:   
        cursor.execute(query, [request_data['course_code']])
        rows = cursor.fetchall()
    a_plan = []
   
    for row in rows:
        
        a_plan.append({
            'component': row[0],
            'mid_sem_exam': row[1],
            'flexible_asssement': row[2],
            'end_semester_exam':row[3],
                      
        })
       
    print(a_plan)
    return {"a_plan":a_plan}


def articulationHelper(request_data):
    slno = 1
    query="""
    select 
    *
    from 
    tb_course_articulation
    where course_code = %s 
    """
        
     # Assuming academic year is calculated as current year + next year (i.e., 2024-2025 for current year 2024)
     #not used
    current_year = datetime.now().year
    
    academic_year = int(str(current_year)[2:] + str(current_year + 1)[2:])  # e.g., 2425 for 2024
    
    with connection.cursor() as cursor:   
        cursor.execute(query, [request_data['course_code']])
        rows = cursor.fetchall()
    
    dataObject = []
    
    
    for row in rows:
        
        dataObject.append({
           'CO_PO': row[0],  # CO_PO will be the first element in each row
            'PO1': row[1],
            'PO2': row[2],
            'PO3': row[3],
            'PO4': row[4],
            'PO5': row[5],
            'PO6': row[6],
            'PO7': row[7],
            'PO8': row[8],
            'PO9': row[9],
            'PO10': row[10],
            'PO11': row[11],
            'PO12': row[12],
            'PSO1': row[13],
            'PSO2': row[14],
            'PSO3': row[15],       
        })
        slno = slno + 1
    print(dataObject)
    
    return {"dataObject":dataObject}