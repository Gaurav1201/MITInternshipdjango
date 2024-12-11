from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .models import tb_users
from datetime import datetime
from django.utils import timezone
from django.db import connection
from rest_framework import status
@api_view( ['GET','POST'])
def add(request):
    print("11111111111111")
    if request.method == 'POST':
        a = request.data.get('a')
        b = request.data.get('b')

        if a is None or b is None:
            return render(request, 'webapp/addition_form.html', {
                'error': "Both 'a' and 'b' must be provided."
            })

        try:
            # Ensure that 'a' and 'b' are numbers
            a = float(a)
            b = float(b)
            result = a + b
            return render(request, 'webapp/addition_form.html', {'result': result})

        except ValueError:
            return render(request, 'webapp/addition_form.html', {
                'error': "'a' and 'b' must be numbers."
            })
    else:
        # For GET request, return the form
        return render(request, 'webapp/addition_form.html')


@api_view(['POST','GET'])  # Change GET to POST since we are adding data to the database
def addData(request):
    #returnData = {"result":"added to db"}
    if request.method == 'POST':
        try:
            user_name = request.data.get("userName", "")
            email_id = request.data.get("emailID", "")
            phone_no = request.data.get("phoneNo", "")
            print(user_name)
            # Check for validation
            if user_name == "" or email_id == "" or len(phone_no) < 10:
                return Response({"message": "Invalid data. Please provide valid user details."}, status=400)
            
            # Save the user details in the database
            user = tb_users.objects.create(
                userName=user_name,
                emailID=email_id,
                phoneNo=phone_no
            )
            # Render the success page with user details and a success message
            return render(request, 'webapp/addition_form.html', {
                "result": "User added successfully!",
                "user_name": user.userName,
                "email_id": user.emailID,
                "phone_no": user.phoneNo
            })


           # return Response({"message": "User created successfully!", "user_id": user.id}, status=201)
        except Exception as e:
            return Response({"error": "An error occurred", "details": str(e)}, status=500)
    else:
        return render(request, 'webapp/addition_form.html')
        
@api_view(['POST','GET'])  # Change GET to POST since we are adding data to the database
def studentDetails(request):
    
    if request.method == 'POST':
        try:
            student_name = request.data.get("student_name", "")
            student_dob = request.data.get("student_dob")
            student_address = request.data.get("student_address")
            email_id = request.data.get("email_id", "")
            phone_no = request.data.get("phone_no", "")
            
            #marks 

            english_marks = int(request.data.get("english_marks"))
            physics_marks = int(request.data.get("physics_marks"))
            chemistry_marks = int(request.data.get("chemistry_marks"))
            # Check for validation
            if False and (student_name == "" or email_id == "" or len(phone_no) < 10 or english_marks <0 or physics_marks <0 or chemistry_marks < 0):
                 return render(request, 'webapp/student_form.html', {
                     "result":False,
                     "message":"Invalid data"
                 })
            
            #calculate percentage

            total = english_marks + physics_marks + chemistry_marks

            percentage = total/3
            
            return render(request, 'webapp/student_form.html', {
                "result":True,
                "message": "Calculated  successfully!",
                "student_name": student_name,
                "student_dob":student_dob,
                "student_address": student_address,
                "email_id": email_id,
                "phone_no": phone_no,
                "english_marks":english_marks,
                "physics_marks": physics_marks,
                "chemistry_marks" : chemistry_marks,
                "percentage":percentage
            })


           # return Response({"message": "User created successfully!", "user_id": user.id}, status=201)
        except Exception as e:
            return Response({"error": "An error occurred", "details": str(e)}, status=500)
    else:
        return render(request, 'webapp/student_form.html')
        
@api_view(['GET', 'POST'])
def empDetails(request):
    if request.method == 'POST':
        gte5yr  = False
        emp_doj = request.data.get("emp_doj", "")

        date_string = '2018-12-10'
        date_string = request.data.get('emp-doj')
        print(date_string)
        # Convert the string to a date object
        date_obj = datetime.strptime(date_string, '%Y-%m-%d').date()

        # Get today's date
        today = timezone.now().date()

        # Calculate the difference in years
        difference_in_years = (today - date_obj).days / 365.25  # 365.25 accounts for leap years

        # Check if the difference is more than 5 years
        if difference_in_years > 5:
            print("The date is more than 5 years ago.")
            gte5yr = True
        else:
            print("The date is less than or equal to 5 years ago.")
            gte5yr = False

        return render(request, 'webapp/employee.html', {
        "result":True,
        "gte5yr":gte5yr
    })

    else:
        return render(request, 'webapp/employee.html')
    

@api_view(['GET'])
def getCourseList(request):
    try:
        # Extract parameters from the GET request query parameters
        faculty_id = request.query_params.get('faculty_id')
        academic_year = request.query_params.get('academic_year')

        # Check if both parameters are provided
        if not faculty_id or not academic_year:
            return Response({
                "result": False,
                "message": "Both faculty_id and academic_year are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # SQL query to fetch course details
        query = """
            SELECT course_id, course_name, course_number
            FROM tb_course
            WHERE faculty_id = %s AND academic_year = %s
        """

        # Execute the query using the database connection
        with connection.cursor() as cursor:
            cursor.execute(query, [faculty_id, academic_year])
            rows = cursor.fetchall()

        # Prepare the response data
        courses = []
        for row in rows:
            courses.append({
                'course_id': row[0],
                'course_name': row[1],
                'course_no': row[2]
            })

        # Response structure
        result = {
            "result": True,
            "message": "Fetched successfully",
            "courses": courses
        }

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        # Catch any exception and return a server error message
        return Response({
            "result": False,
            "message": f"An error occurred: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getLessonPlan(request):
    try:
        # Extract parameters from the GET request query parameters
        course_id = request.query_params.get('course_id')
        academic_year = request.query_params.get('academic_year')

        # Check if both parameters are provided
        if not course_id or not academic_year:
            return Response({
                "result": False,
                "message": "Both course_id and academic_year are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        # SQL query to fetch lesson plan details
        query = """
            SELECT id, lesson_id, description, course_no, course_id
            FROM tb_lesson_plan
            WHERE course_id = %s AND academic_year = %s
        """

        # Execute the query using the database connection
        with connection.cursor() as cursor:
            cursor.execute(query, [course_id, academic_year])
            rows = cursor.fetchall()

        # Prepare the response data
        lesson_plan = []
        for row in rows:
            lesson_plan.append({
                'id': row[0],
                'lesson_id': row[1],
                'description': row[2],
                'course_no': row[3],
                'course_id': row[4],
            })

        # Return the response with the fetched data
        result = {
            "result": True,
            "message": "Fetched successfully",
            "lesson_plan": lesson_plan
        }

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        # Catch any exception and return a server error message
        return Response({
            "result": False,
            "message": f"An error occurred: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def uploadStudentList(request):
    try:
        # Extract parameters from the GET request query parameters
        
        academic_year = request.data.get('academic_year')
        programme_name = request.data.get('programme_name')
        student_list = []
        # Check if both parameters are provided
        if not academic_year or not programme_name:
            return Response({
                "result": False,
                "message": "Both academic_year and programme_year are required."
            }, status=status.HTTP_400_BAD_REQUEST)

        if 'file' not in request.FILES:
             return Response({
                "result": False,
                "message": "File not attached."
            }, status=status.HTTP_400_BAD_REQUEST)
        

        # Get the uploaded file
        excel_file = request.FILES.get('file')
        if excel_file:
            try:
                workbook = openpyxl.load_workbook(excel_file)
                sheet = workbook.active
                for i, row in enumerate(sheet.iter_rows(min_row = 2, values_only = True)):
                    roll_no, name = row
            except Exception as e:
                print("1")
        query = """
            SELECT id, lesson_id, description, course_no, course_id
            FROM tb_lesson_plan
            WHERE course_id = %s AND academic_year = %s
        """

        # Execute the query using the database connection
        with connection.cursor() as cursor:
            cursor.execute(query, [course_id, academic_year])
            rows = cursor.fetchall()

        # Prepare the response data
        lesson_plan = []
        for row in rows:
            lesson_plan.append({
                'id': row[0],
                'lesson_id': row[1],
                'description': row[2],
                'course_no': row[3],
                'course_id': row[4],
            })

        # Return the response with the fetched data
        result = {
            "result": True,
            "message": "Fetched successfully",
            "lesson_plan": lesson_plan
        }

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        # Catch any exception and return a server error message
        return Response({
            "result": False,
            "message": f"An error occurred: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


