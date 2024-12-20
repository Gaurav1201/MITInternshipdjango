from django.urls import path  # Use path() instead of url()
from . import views

urlpatterns = [
    path('addition/', views.add, name='addition'),  # Use path() for routing
    path('addData/', views.addData, name='addData'),  
    path('studentDetails/', views.studentDetails, name='studentDetails'),
    path('empDetails/', views.empDetails, name='empDetails'),

    path('getcourselist/', views.getCourseList, name='getCourseList'),
    path('getlessonplan/', views.getLessonPlan, name='getLessonPlan'),
    path('addfacultyrow/', views.addFacultyRow, name='addFacultyRow'),
    path('uploadfacultylist/', views.uploadFacultyList, name='uploadFacultyList'),
    path('uploadcoursefacultymapping/', views.uploadCourseFacultyMapping, name='uploadCourseFacultyMapping'),
    path('getfacultylist/', views.getFacultyList, name='getFacultyList'),
    path('addCourseDetails/', views.addCourseDetails, name='addCourseDetails'),
    path('converttopdf/', views.convertToPDF, name='convertToPDF'),
    path('getcourselistpage/', views.getCourseListPage, name='getCourseListPage'),
    path('getpdfpage/', views.getPdfPage, name='getPdfPage'),
    path('getCourseOutcomes/', views.getCourseOutcomes, name='getCourseOutcomes'),
    path('getCourseOutcomesPage/', views.getCourseOutcomesPage, name='getCourseOutcomesPage'),
    path('add_course_outcome/', views.add_course_outcome_api, name='add_course_outcome_api'),
    path('updateCourseOutcome/<int:id>/', views.updateCourseOutcome, name='updateCourseOutcome'),
    path('getassementplanpage/', views.getAssementPlanPage, name='getAssementPlanPage'),
    path('getassementplan/', views.getAssementPlan, name='getAssementPlan'),
]
