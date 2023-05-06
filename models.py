
from urllib import request
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"), (4,"Parent"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)

class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class courses(models.Model):
    course_id=models.IntegerField(primary_key=True)
    Name=models.CharField(max_length=25)
    dept=models.CharField(max_length=30)
    objects = models.Manager()

class staff(models.Model):
    staff_id = models.IntegerField(unique=True,null=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    staff_name=models.CharField(max_length=25)
    course_id=models.ForeignKey(courses,on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class stud(models.Model):
    rno = models.IntegerField(unique=True,null=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sclass = models.CharField(max_length=25)
    section  = models.CharField(max_length=10)
    gender = models.CharField(max_length=50)
    DOB = models.DateField(default='1998-01-01')
    profile_pic=models.ImageField(upload_to='media/')
    academic_advisor=models.CharField(max_length=25)
    father_name = models.CharField(max_length=50)
    mother_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=10)
    address= models.CharField(max_length=50)
    achievements=models.CharField(max_length=100)
    scholarship=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    midday_meal=models.CharField(max_length=20)
    course=models.CharField(max_length=10,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class parent(models.Model):
    parent_id=models.IntegerField(unique=True,null=True)
    admin = models.OneToOneField(CustomUser, on_delete = models.CASCADE)
    rno=models.ForeignKey(stud,on_delete=models.CASCADE,null=True)
#   rno = models.IntegerField()
    parent_name=models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact=models.CharField(max_length=10)
    objects = models.Manager()

class classes(models.Model):
    class_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=15)
    course_id=models.ForeignKey(courses,on_delete=models.CASCADE)
    objects = models.Manager()

class subjects(models.Model):
    staff_id=models.ForeignKey(staff,on_delete=models.CASCADE)
    subject_id=models.IntegerField(primary_key=True,max_length=20)
    subject=models.CharField(max_length=50)
    class_id=models.ForeignKey(classes,on_delete=models.CASCADE)
    objects = models.Manager()

class mark(models.Model):
    mid=models.ForeignKey(stud,on_delete=models.CASCADE)
    rno=models.IntegerField()
    subject_id=models.ForeignKey(subjects,on_delete=models.CASCADE)
    marks=models.CharField(max_length=3)
    category=models.CharField(max_length=20)
    objects = models.Manager()

class attendance(models.Model):
    attendance_id=models.AutoField(primary_key=True)
    rid=models.ForeignKey(stud,on_delete=models.CASCADE)
    rno=models.IntegerField(null=True)
    subject_id=models.ForeignKey(subjects,on_delete=models.CASCADE,null=True)
    attendance_date=models.DateField(null=True)
    status=models.IntegerField(default=0)
    objects = models.Manager()
    
class application(models.Model):
    appn_id=models.AutoField(primary_key=True)
    id=models.ForeignKey(stud,on_delete=models.CASCADE)
    rno=models.IntegerField()
    distance=models.CharField(max_length=3)
    income_status=models.CharField(max_length=10)
    appn_status=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class leave(models.Model):
    leave_id=models.AutoField(primary_key=True)
    id=models.ForeignKey(stud,on_delete=models.CASCADE)
    rno=models.IntegerField()
    staff_id=models.IntegerField()
    leave_reason=models.CharField(max_length=100)
    leave_date=models.DateField()
    leave_status=models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class notification(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.IntegerField(null=True)
    parent_id = models.IntegerField(null=True)
    parent_message = models.TextField()
    messages = models.TextField()
    staff_id=models.IntegerField()
    staff_name=models.CharField(max_length=25)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class query(models.Model):
    id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey(parent, on_delete=models.CASCADE)
    querys = models.TextField()
    staff_id=models.IntegerField()
    query_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class feedback(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(stud, on_delete=models.CASCADE)
    feedbacks = models.TextField()
    staff_id = models.IntegerField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            staff.objects.create(admin=instance,staff_name="",course_id=None,staff_id=None)
        if instance.user_type == 3:
            stud.objects.create(admin=instance,gender="",first_name="",last_name="",email="",section="",course=None,rno=None,sclass="")
        if instance.user_type == 4:
            parent.objects.create(admin=instance,parent_name="",parent_id=None,rno=None,contact="")

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.stud.save()
    if instance.user_type == 4:
        instance.parent.save()
    