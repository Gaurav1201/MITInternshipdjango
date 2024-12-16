from django.urls import path  # Use path() instead of url()
from . import views

urlpatterns = [
    path('addition/', views.add, name='addition'),  # Use path() for routing
    path('addData/', views.addData, name='addData'),  
    path('studentDetails/', views.studentDetails, name='studentDetails'),
    path('empDetails/', views.empDetails, name='empDetails'),

    path('getcourselist/', views.getCourseList, name='getCourseList'),
    path('getlessonplan/', views.getLessonPlan, name='getLessonPlan'),
    path('uploadfacultylist/', views.uploadFacultyList, name='uploadFacultyList'),
    path('uploadcoursefacultymapping/', views.uploadCourseFacultyMapping, name='uploadCourseFacultyMapping'),
    path('getfacultylist/', views.getFacultyList, name='getFacultyList'),
    path('addCourseDetails/', views.addCourseDetails, name='addCourseDetails'),
    path('converttopdf/', views.convertToPDF, name='convertToPDF'),
    path('getcourselistpage/', views.getCourseListPage, name='getCourseListPage'),
]
