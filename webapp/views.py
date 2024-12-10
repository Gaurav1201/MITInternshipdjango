from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import tb_users
@api_view( ['GET','POST'])
def add(request):
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
        