from django.db import models

# Create your models here.
from django.db import models

class tb_users(models.Model):
    userName = models.CharField(max_length=100)
    emailID = models.EmailField(unique=True)
    phoneNo = models.CharField(max_length=15)

    def __str__(self):
        return self.userName
    
class tb_user_new(models.Model):
    userName1 = models.CharField(max_length=100)
    emailId1 = models.EmailField(unique=True)
    phoneNo1 = models.CharField(max_length=15)

    def __str__(self):
        return self.userName1