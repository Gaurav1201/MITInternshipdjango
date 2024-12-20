from django.db import models



# class tb_users(models.Model):
#     userName = models.CharField(max_length=100)
#     emailID = models.EmailField(unique=True)
#     phoneNo = models.CharField(max_length=15)

#     def __str__(self):
#         return self.userName
    
# class tb_user_new(models.Model):
#     userName1 = models.CharField(max_length=100)
#     emailId1 = models.EmailField(unique=True)
#     phoneNo1 = models.CharField(max_length=15)

#     def __str__(self):
#         return self.userName1

class tb_roles(models.Model):
    role_id = models.AutoField(primary_key=True)  # Auto incremented primary key
    role_name = models.CharField(max_length=45, null=True, blank=True)
    faculty = models.CharField(max_length=45, null=True, blank=True)

    class Meta:
        db_table = 'tb_roles'  # Specify the table name

    def __str__(self):
        return self.role_name or "No Name"

class tb_faculty(models.Model):
    seniority = models.IntegerField(null=False)
    faculty_id = models.CharField(max_length=45, primary_key=True)
    faculty_name = models.CharField(max_length=255, null=False)
    faculty_password = models.CharField(max_length=50, null=False)
    role_id = models.IntegerField()  # Storing role_id as an integer, no foreign key
    designation = models.CharField(max_length=45, null=False)

    class Meta:
        db_table = 'tb_faculty'  # The table name in MySQL

    def __str__(self):
        return self.faculty_name


class tb_course(models.Model):
    course_code = models.CharField(max_length=45,primary_key=True,default='DEFAULT_CODE')
    course_name = models.CharField(max_length=255)
    course_description = models.TextField(blank=True, null=True) 
    course_references = models.CharField(max_length=255)
    course_programme = models.CharField(max_length=45)
    course_sem = models.IntegerField()
    lecture_hour = models.IntegerField(default=3)
    tutorial_hour = models.IntegerField(default=1)
    p = models.IntegerField(default=3)
    c = models.IntegerField(default=4)
    class Meta:
        db_table = 'tb_course'  # The table name in MySQL

    def __str__(self):
        return self.course_name
# class lessonplan(models.Model):
#     lsid = models.CharField(max_length=20)
#     descp = models.CharField(max_length=255)
#     cosn = models.CharField(max_length=20)

#     class Meta:
#         db_table = 'lessonplan' #anirudhs db schema for lessonplan
class tb_lesson_plan(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing primary key
    lesson_id = models.CharField(max_length=10)  # Unique lesson_id
    description = models.CharField(max_length=255)  # Lesson description
    co_num = models.CharField(max_length=5)  # CO number
    course_code = models.CharField(max_length=45)  # Course ID
    academic_year = models.IntegerField()
    class Meta:
        db_table = 'tb_lesson_plan'  # The table name in MySQL

    def __str__(self):
        return f"Lesson Plan {self.lesson_id} for Course {self.course_id}"

class tb_student(models.Model):
    student_id = models.CharField(max_length=10, primary_key=True)  # `student_id` as varchar(10)
    student_name = models.CharField(max_length=255)
    student_programme = models.CharField(max_length=45)
    student_branch = models.CharField(max_length=45)

    class Meta:
        db_table = 'tb_student'  # Table name in MySQL

    def __str__(self):
        return self.student_name
    


class tb_course_faculty_mapping(models.Model):
    course_code = models.CharField(max_length=45, primary_key=False)  
    faculty_id = models.CharField(max_length=45)
    academic_year = models.IntegerField()
   
    class Meta:
        db_table = 'tb_course_faculty_mapping'  # Table name in MySQL

    def __str__(self):
        return self.student_name
    

    
class tb_AssessmentPlan(models.Model):
    component = models.CharField(max_length=50, primary_key=True)
    mid_sem_exam = models.TextField(null=True, blank=True)
    flexible_assessments = models.TextField(null=True, blank=True)
    end_semester_exam = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'tb_AssessmentPlan'  # The table name in MySQL
        


class tb_course_outcome(models.Model):
    # ID field is automatically created as a primary key
    id = models.BigAutoField(primary_key=True)  # Equivalent to `bigint NOT NULL AUTO_INCREMENT`
    
    # Fields mapping to the columns in the SQL table
    co_num = models.CharField(max_length=5)  # Equivalent to `varchar(255)`
    description = models.TextField()  # Equivalent to `longtext`
    contact_hours = models.PositiveIntegerField()  # Equivalent to `int unsigned`
    marks = models.DecimalField(max_digits=5, decimal_places=2)  # Equivalent to `decimal(5,2)`
    course_code = models.CharField(max_length=45)
    # Constraint to check that contact_hours is greater than or equal to 0
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(contact_hours__gte=0),
                name='contact_hours_gte_0'
            )
        ]

    def __str__(self):
        return self.id
    
class tb_course_articulation(models.Model):
    CO_PO = models.CharField(max_length=10)  # Corresponds to varchar(10)
    PO1 = models.IntegerField(null=True, blank=True)  # Corresponds to int
    PO2 = models.IntegerField(null=True, blank=True)
    PO3 = models.IntegerField(null=True, blank=True)
    PO4 = models.IntegerField(null=True, blank=True)
    PO5 = models.IntegerField(null=True, blank=True)
    PO6 = models.IntegerField(null=True, blank=True)
    PO7 = models.IntegerField(null=True, blank=True)
    PO8 = models.IntegerField(null=True, blank=True)
    PO9 = models.IntegerField(null=True, blank=True)
    PO10 = models.IntegerField(null=True, blank=True)
    PO11 = models.IntegerField(null=True, blank=True)
    PO12 = models.IntegerField(null=True, blank=True)
    PSO1 = models.IntegerField(null=True, blank=True)
    PSO2 = models.IntegerField(null=True, blank=True)
    PSO3 = models.IntegerField(null=True, blank=True)
    course_code = models.CharField(max_length=45)
    def __str__(self):
        return self.CO_PO

class tb_course_outcomes(models.Model):
    id = models.BigAutoField(primary_key=True)
    co_num = models.CharField(max_length=255)
    description = models.TextField()
    contact_hours = models.PositiveIntegerField()  # Ensures non-negative integers
    marks = models.IntegerField()
    program_outcomes = models.CharField(max_length=15)
    program_spec_outcomes = models.CharField(max_length=50)
    learning_outcomes = models.CharField(max_length=20)
    bl = models.CharField(max_length=10)
    course_code = models.CharField(max_length=45)

    class Meta:
        db_table = 'tb_course_outcomes'  # Optional: matches the table name in the database
        constraints = [
            models.CheckConstraint(check=models.Q(contact_hours__gte=0), name='tb_course_outcomes_chk_1'),
        ]

    def __str__(self):
        return f"{self.co_num}: {self.description[:50]}..."  # Truncate for readability