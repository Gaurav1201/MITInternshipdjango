from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from datetime import datetime
from django.utils import timezone
from django.db import connection
from rest_framework import status
import pandas as pd
from fpdf import FPDF
import pydf
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import weasyprint
import os
from django.template.loader import render_to_string
from .helper import *
from django.db.models  import Max, F

from .serializers import CourseOutcomeSerializer

globalFunctionMapper = {
    "course_description": courseDescriptionHelper,
    "lesson_plan": lessonPlanHelper,
    "course_outcomes": courseOutcomesHelper,
    "assesement_plan": assesementPlanHelper,
    "references": referencesHelper,
    "course_articulation": articulationHelper
}

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
        print(faculty_id) 
        current_year = datetime.now().year
        
        # Assuming academic year is calculated as current year + next year (i.e., 2024-2025 for current year 2024)
        academic_year = int(str(current_year)[2:] + str(current_year + 1)[2:])  # e.g., 2425 for 2024
        print(academic_year)
      #  academic_year = 2425
        #academic_year = request.query_params.get('academic_year')

        # Check if both parameters are provided
        if not faculty_id or not academic_year:
            return Response({
                "result": False,
                "message": "Both faculty_id and academic_year are required."
            }, status=status.HTTP_200_OK)

        # SQL query to fetch course details
        query = """
            SELECT
            cm.course_code , cs.course_name , cm.faculty_id, cs.course_description
            FROM
            tb_course_faculty_mapping cm, tb_course cs 
            WHERE
            cm.course_code = cs.course_code
            AND
            cm.faculty_id = %s 
            AND
            cm.academic_year = %s
        """

        # Execute the query using the database connection
        with connection.cursor() as cursor:
            cursor.execute(query, [faculty_id, academic_year])
            rows = cursor.fetchall()

        # Prepare the response data
        courses = []
        for row in rows:
            courses.append({
                'course_code': row[0],
                'course_name': row[1],
                'faculty_id': row[2],
                'course_description': row[3]
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
        }, status=status.HTTP_200_OK)

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
            }, status=status.HTTP_200_OK)

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
        }, status=status.HTTP_200_OK)
    
@api_view(['POST', 'GET'])
def uploadFacultyList(request):
    if request.method == 'POST':
        try:
            # Get the uploaded file
            excel_file = request.FILES['file']
            print(f"Received file: {excel_file.name}")

            # Check if the file has the correct extension
            if not excel_file.name.endswith(('.xlsx', '.xls')):
                return JsonResponse({
                    "result": False,
                    "message": "Invalid file format. Please upload an Excel file."
                })

            # Use pandas to read the Excel file
            df = pd.read_excel(excel_file)
            print(f"Data read from Excel: {df}")

            # Initialize variables to store error and success information
            existing_faculty_ids = set(tb_faculty.objects.values_list('faculty_id', flat=True))
            error_rows = []  # List to track existing faculty IDs
            uploaded_rows = []  # List to track successfully uploaded records

            used_seniorities = set(tb_faculty.objects.values_list('seniority', flat=True))

            # Loop through the rows of the DataFrame
            for index, row in df.iterrows():
                # Extract data from the row
                seniority = row.get('Sl.No')
                faculty_id = row.get('ID')
                faculty_name = row.get('Name of the Faculty', '')
                faculty_designation = row.get('Designation', '')

                # Skip if faculty_id or seniority is missing or invalid
                if pd.isna(faculty_id) or pd.isna(seniority):
                    continue

                conflicting_records = tb_faculty.objects.filter(seniority__gte=seniority).order_by('seniority')

                if conflicting_records.exists():
                # Step 2: Shift the seniority of existing records in ascending order
                    for record in conflicting_records:
                    # Only increment seniority if the record's seniority is >= excel_seniority
                        if record.seniority >= seniority:
                            record.seniority += 1
                            record.save()



                # Check if the faculty ID already exists
                if faculty_id in existing_faculty_ids:
                    # If the faculty ID exists, add to the error list
                    error_rows.append(faculty_id)
                else:
                    # If faculty ID does not exist, add to the database and track success
                    tb_faculty.objects.create(
                        seniority=seniority,
                        faculty_id=faculty_id,
                        faculty_name=faculty_name,
                        faculty_password="Manipal@123",  # Default password
                        role_id=1,
                        designation=faculty_designation
                    )
                    uploaded_rows.append(faculty_id)

                used_seniorities.add(seniority)

            # Prepare messages based on the result
            if error_rows:
                error_message = f"Some faculty IDs already exist in the database:\n" + "\n".join(map(str, error_rows))
                success_message = f"{len(uploaded_rows)} records successfully uploaded!"
                return JsonResponse({
                    "result": False,
                    "message": error_message + "\n\n" + success_message
                })

            success_message = f"Successfully uploaded {len(uploaded_rows)} records!"
            return JsonResponse({
                "result": True,
                "message": success_message
            })

        except Exception as e:
            # Print the error and traceback
            print(f"Error: {e}")
            return JsonResponse({
                "result": False,
                "message": f"An error occurred while uploading the file: {str(e)}"
            })
    else:
        return render(request, "webapp/facultyExcelUpload.html")



@api_view(['GET'])
def getFacultyList(request):
    try:
        # SQL query to fetch faculty details
        query = """
            SELECT seniority, faculty_id, faculty_name, designation
            FROM tb_faculty
            ORDER BY seniority
        """

        # Execute the query using the database connection
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        # Prepare the response data
        faculty_list = []
        for row in rows:
            faculty_list.append({
                'seniority': row[0],
                'faculty_id': row[1],
                'faculty_name': row[2],
                'designation': row[3]
            })

        # Response structure
        result = {
            "result": True,
            "message": "Fetched successfully",
            "faculty_list": faculty_list
        }

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        # Catch any exception and return a server error message
        return Response({
            "result": False,
            "message": f"An error occurred: {str(e)}"
        }, status=status.HTTP_200_OK)

@api_view(['POST'])
def addFacultyRow(request):
    if request.method == 'POST':
        try:
            # Extract form data
            faculty_id = request.POST.get('facultyID', None)
            faculty_name = request.POST.get('facultyName', None)
            designation = request.POST.get('designation', None)
            seniority = request.POST.get('seniority', None)

            # Ensure required fields are provided
            if not all([faculty_id, faculty_name, designation, seniority]):
                return JsonResponse({
                    "result": False,
                    "message": "All fields (Faculty ID, Name, Designation, Seniority) are required."
                })

            # Check if the faculty ID already exists
            if tb_faculty.objects.filter(faculty_id=faculty_id).exists():
                return JsonResponse({
                    "result": False,
                    "message": f"Faculty ID '{faculty_id}' already exists in the database."
                })

            # Additional seniority validation (if applicable)
            max_seniority = tb_faculty.objects.aggregate(Max('seniority'))['seniority__max'] or 0
            if int(seniority) > max_seniority + 1:
                return JsonResponse({
                    "result": False,
                    "message": f"Seniority can't exceed {max_seniority + 1}."
                })

            # Update seniority of existing records
            tb_faculty.objects.filter(seniority__gte=int(seniority)).update(
                seniority=F('seniority') + 1
            )

            # Create the new faculty record
            tb_faculty.objects.create(
                faculty_id=faculty_id,
                faculty_name=faculty_name,
                designation=designation,
                seniority=seniority,
                faculty_password="Manipal@123",  # Default password
                role_id=2  # Assuming role_id is 2 for non-admin faculty
            )

            return JsonResponse({
                "result": True,
                "message": "Faculty member added successfully."
            })

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({
                "result": False,
                "message": "An error occurred while adding the faculty member."
            })

@api_view(['GET', 'POST'])
def uploadCourseFacultyMapping(request):
    if request.method == 'POST':
        try:
            # POST Data
            academic_year = request.data.get('academic_year')
            # Get the uploaded file
            excel_file = request.FILES['file']
            print(excel_file)

            # Check if the file has the correct extension
            if not excel_file.name.endswith('.xlsx') and not excel_file.name.endswith('.xls'):
                return render(request, 'webapp/courseFacultyMaping.html', {
                    "result": False,
                    "message": "File not proper"
                })

          
            df = pd.read_excel(excel_file)
            print(df)


           # df = pd.read_excel('your_file.xlsx', header=None)

            # Initialize an empty list to store the rows as nested arrays
            nested_array = []

            # Iterate through each row and extract all column data as a list
            for index, row in df.iterrows():
                row_data = row.tolist()  # Convert the row (Series) to a list
                nested_array.append(row_data)
            

            for i in range(0, len(nested_array)):
                for j in range (1,len(nested_array[i])):
                    faculty_id = nested_array[i][0]
                    course_code = nested_array[i][j]
                    if pd.isna(course_code) or pd.isna(faculty_id):
                         continue  
                    tb_course_faculty_mapping.objects.create(
                    course_code = course_code,
                    faculty_id=faculty_id,
                    academic_year = 2425
                )
            # Loop through the rows of the DataFrame and save to the database
            

            return render(request, 'webapp/courseFacultyMaping.html', {
                "result": True,
                "message": "Data successfully uploaded!"
            })

        except Exception as e:
            print(f"Error: {e}")
            return render(request, 'webapp/courseFacultyMaping.html', {
                "result": False,
                "message": "Error occurred while uploading the file."
            })
    else:
        return render(request, 'webapp/courseFacultyMaping.html')
    
@api_view(['POST'])
def addFacultyRow(request):
    if request.method == 'POST':
        try:
            # Extract form data from the POST request
            seniority = request.POST.get('seniority', None)
            faculty_id = request.POST.get('facultyID', None)
            faculty_name = request.POST.get('facultyName', None)
            designation = request.POST.get('designation', None)
            # Assuming faculty is non-admin
            role = 2

            # Ensure all fields are provided
            if not all([faculty_id, faculty_name, designation]):
                return Response({
                    "result": False,
                    "message": "All fields (Faculty ID, Name, Designation) are required."
                })

            # Query to get the max seniority value
            query_seniority = "SELECT MAX(seniority) FROM tb_faculty"
            
            # Execute the query to get the current max seniority
            with connection.cursor() as cursor:
                cursor.execute(query_seniority)
                rows = cursor.fetchall()

            # Ensure we have a result from the query
            if rows and rows[0][0] is not None:
                max_seniority = int(rows[0][0])
            else:
                max_seniority = 0  # If no records exist, max seniority would be 0

            # Check if the seniority value is within acceptable range
            if int(seniority) > max_seniority + 1:
                return Response({
                    "result": False,
                    "message": f"Seniority can be at max {max_seniority + 1}!"
                })
            
            # Update the seniority of existing faculty records if necessary
            query_update_seniority = "UPDATE tb_faculty SET seniority = seniority + 1 WHERE seniority >= %s"
            with connection.cursor() as cursor:
                cursor.execute(query_update_seniority, [int(seniority)])

            # Create a new faculty record in the database
            tb_faculty.objects.create(
                seniority=seniority,
                faculty_id=faculty_id,
                faculty_name=faculty_name,
                faculty_password="Manipal@123",  # Default password 
                role_id=role,  # Assuming role_id is 2 for non-admin faculty
                designation=designation
            )

            # Return success response
            return Response({
                "result": True,
                "message": "Faculty member added successfully!"
            })
        except Exception as e:
            # Log and return error response
            print(f"Error: {e}")
            return Response({
                "result": False,
                "message": "An error occurred while adding the faculty member."
            })
        
@api_view(['PATCH'])
def addCourseDetails(request):
    if request.method == 'PATCH':
        try:
            # Extract form data from the POST request
            course_code = request.data.get('course_code', None)
           # course_name = request.data.get('course_name', None)
            course_description = request.data.get('course_description', None)
            
            # Ensure all fields are provided
            if not all([course_code,course_description]):
                return Response({
                    "result": False,
                    "message": "All fields are required."
                })

            # Query to get the max seniority value
            query_add = "UPDATE tb_course SET course_description = %s WHERE course_code = %s"
            
            # Execute the query to get the current max seniority
            with connection.cursor() as cursor:
                cursor.execute(query_add,[course_description, course_code])
            
            # Return success response
            return Response({
                "result": True,
                "message": "Course updated successfully!"
            })
        except Exception as e:
            # Log and return error response
            print(f"Error: {e}")
            return Response({
                "result": False,
                "message": "An error occurred while adding course description."
            })
        
        
#This function is built to reduce the redundancy, instead of creating the api for different page, it uses only 1 appi which takes the data to be printed 
# and the name of the page, it will then map the page name with a pre defined dictionary which will then redirected to the secified page with the data
#this way you dont need to have many apis
@api_view(['POST'])
def convertToPDF(request):
    print(request.data)
    # Get data from request
    #faculty_id = request.data.get('faculty_id')
    # course_code = request.data.get('course_code')
    # course_name = request.data.get('course_name')
    # page_name = request.data.get('page_name')
    # description = request.data.get('description')

    # Render HTML template with the form data
    # html_content = render_to_string('webapp/toPDFcourse_description.html', {
    #    # 'faculty_id': faculty_id,
    #     'course_code': course_code,
    #     'course_name': course_name,
    #     'course_description': description,
    # })
    
    # Render HTML template with the form data
    
    # Get the page name from request.data
    page_name = request.data.get('page_name')
    file_dest = 'webapp/toPDF'+page_name+'.html'
    #Call the helper function
    
   # data = courseDescriptionHelper(request.data.get('course_code'))
    data = globalFunctionMapper[page_name](request.data)
    print(data)
    html_content = render_to_string(file_dest, data)
    # html_content = render_to_string(str_desti, request.data)
    # html_content = render_to_string('webapp/toPDFcourse_description.html', request.data)
    
    # Convert the rendered HTML to PDF using WeasyPrint
    pdf_file = weasyprint.HTML(string=html_content).write_pdf()
    
    # Return the PDF as an HTTP response
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+page_name+'.pdf"'

    return response

# Call the function to create the PDF
  
#    return Response({
#                 "result": True,
#                 "message": "true"
#             })
   

@api_view(['GET'])
def getCourseListPage(request):
    #  return render(request, 'webapp/sample.html', {
    #             'result': True,
    #             "message":"True."
    #     })
      return render(request, 'webapp/addCourseDetails.html', {
                'result': True,
                "message":"True."
        })
      
@api_view(['GET'])
def getPdfPage(request):
    
    return render(request, 'webapp/generatePDF.html', {
                'result': True,
                "message":"True."
        })
    

@api_view(['GET'])
def getCourseOutcomesPage(request):
    return render(request, 'courses/course_outcome.html')  # Render form template for GET requests


@api_view(['POST'])
def add_course_outcome_api(request):
    if request.method == 'POST':
        serializer = CourseOutcomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Course outcome added successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def updateCourseOutcome(request,id):
    try:
        # Get parameters from the request
        # id = request.query_params.get('id')
        contact_hours = request.data.get('contact_hours')
        marks = request.data.get('marks')

        if not id or contact_hours is None or marks is None:
            return Response({"result": False, "message": "Missing required parameters"}, status=status.HTTP_400_BAD_REQUEST)

        # Update query
        query = "UPDATE tb_course_outcomes SET contact_hours = %s, marks = %s WHERE id = %s"

        with connection.cursor() as cursor:
            cursor.execute(query, [contact_hours, marks, id])
            rows = cursor.fetchall()

        if rows:
            return Response({"result": False, "message": "Course outcome not found"}, status=status.HTTP_404_NOT_FOUND)

        # Return success response
        result = {
            "result": True,
            "message": "Updated successfully",
        }

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        # Log the exception (optional)
        print(f"Error occurred: {e}")
        
        # Return error response
        return Response({"result": False, "message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

@api_view(['GET'])
def getAssementPlanPage(request):
    return render(request, 'webapp/assement_planMTech.html')
    if request.query_params.get('programme') == 'BTech':
        return render(request, 'webapp/assement_planBTech.html')  # Render form template for GET requests
    else:
        return render(request, 'webapp/assement_planMTech.html')  # Render form template for GET requests

@api_view(['GET'])
def getCourseOutcomes(request):
    try:
        # Get faculty ID and role ID
        faculty_id = request.query_params.get('faculty_id')
        role_id = request.query_params.get('role_id')
        print(role_id)
        print(faculty_id)
        
        whereClause = ' WHERE 1=1 '
        if role_id == '2' or role_id=='3':  # Ensure role_id is compared as a string
            # Sanitize faculty_id to prevent SQL injection
            faculty_id = str(faculty_id).replace("'", "''")
            whereClause = f" WHERE course_code IN (SELECT course_code FROM tb_course_faculty_mapping WHERE faculty_id = '{faculty_id}')"
        
        # Construct the query
        query = f"""
            SELECT co_num, description, contact_hours, marks, program_outcomes, program_spec_outcomes, bl, course_code,id
            FROM tb_course_outcomes
            {whereClause}
            ORDER BY id
        """

        # Execute the query using the database connection
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        # Debugging: Print the fetched rows
      #  print("Fetched rows:", rows)

        # Prepare the response data
        course_outcome = []

        for row in rows:
            course_outcome.append({
                'co_num': row[0],
                'description': row[1],
                'contact_hours': row[2],
                'marks': row[3],
                'program_outcomes': row[4],
                'program_spec_outcomes': row[5],
                'bl': row[6],
                'course_code': row[7],
                'id':row[8]
            })
        print(course_outcome)
        # Response structure
        result = {
            "result": True,
            "message": "Fetched successfully",
            "course_outcome": course_outcome
        }

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        # Debugging: Log the exception
        print("Error occurred:", str(e))
        return Response({
            "result": False,
            "message": f"An error occurred: {str(e)}"
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def getAssementPlan(request):
    
    try:
    # Get programme and course codeID
        #programme = request.query_params.get('programme')
        # if programme == "MTech":
        #     table_name = 'tb_AssessmentPlanMtech'
        # else:
        #     table_name = "tb_AssementPlanBTech"
        table_name = "tb_AssesmentPlanMTech"
        course_code = request.query_params.get('course_code','CSE5117')
        query=f"""
        select 
        component, mid_sem_exam,flexible_assessments,end_semester_exam, ap_id
        from 
        {table_name}
        where course_code = %s 
        """
        
     # Assuming academic year is calculated as current year + next year (i.e., 2024-2025 for current year 2024)
     #not used
        current_year = datetime.now().year
    
        academic_year = int(str(current_year)[2:] + str(current_year + 1)[2:])  # e.g., 2425 for 2024
    
        with connection.cursor() as cursor:   
            cursor.execute(query, [course_code])
            rows = cursor.fetchall()
        a_plan = []
   
        for row in rows:
        
            a_plan.append({
            'component': row[0],
            'mid_sem_exam': row[1],
            'flexible_asssement': row[2],
            'end_semester_exam':row[3],
            'id':row[4]
                      
        })        # Response structure
        print(a_plan)
        result = {
            "result": True,
            "message": "Fetched successfully",
            "a_plan": a_plan
        }

        return Response(result, status=status.HTTP_200_OK)

    except Exception as e:
        # Debugging: Log the exception
        print("Error occurred:", str(e))
        return Response({
            "result": False,
            "message": f"An error occurred: {str(e)}"
        }, status=status.HTTP_200_OK)

