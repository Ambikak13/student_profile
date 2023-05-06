from django.shortcuts import render
from email import message
import email
from multiprocessing import context
from tokenize import Name
from unicodedata import category
from urllib import request
from venv import create
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect 
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate
from myapp.EmailBackEnd import EmailBackEnd
from django.db.models import Max
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from django.db.models import Max,Sum,Count
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def some(request):
    return render(request,"s1/login.html")

def signin(request):
  if request.method=="GET":
        # user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
        if request.user:
            user_type = request.user.user_type
            if user_type == '1':
                return render(request,"s1/admin.html")
                
            elif user_type == '2':
                return render(request,"s1/staff.html")
                
            elif user_type == '3':
                return render(request,"s1/student.html")
            else:
               return render(request,"s1/parent.html")
        else:
            messages.error(request, "Invalid Credentials!")
            return HttpResponseRedirect("/some/")
        
        # return HttpResponse("<h2>Method Not Allowed</h2>")
  if request.method=="POST":
    user = EmailBackEnd.authenticate(request, username=request.POST.get('email'), password=request.POST.get('password'))
    if user != None:
      login(request, user)
      user_type = user.user_type
      if user_type == '1':
        return render(request,"s1/admin.html")
                
      elif user_type == '2':
        return render(request,"s1/staff.html")
                
      elif user_type == '3':
        return render(request,"s1/student.html")
      else:
        return render(request,"s1/parent.html")
    else:
        messages.error(request, "Invalid Credentials!")
        return HttpResponseRedirect("/some/")
            # return redirect('login')


def add_course(request):
  if courses.objects.all().count()==0:
    cid=1
  else:
    cid=courses.objects.aggregate(max=Max("course_id"))["max"]+1
  return render(request,"s1/addcourse.html",{"cid":cid})

def add_course_save(request):
  if request.method!="POST":
    return HttpResponse(request,"Method not allowd")
  else:
    course=request.POST.get("Name")
    cid=request.POST.get("course_id")
    dept=request.POST.get("dept")
    try:
      if courses.objects.filter(course_id=cid).exists():
        messages.error(request,"Failed to add Course!! Course ID already exists")
      elif courses.objects.filter(Name=course).exists():
        messages.error(request,"Failed to add Course!! Course already exists")
      else:
        course_model=courses(course_id=cid,Name=course,dept=dept)
        course_model.save()
        messages.success(request,"Successfuly added course")
    except:
      messages.error(request,"Failed to add course")
    return redirect("add_course")

def manage_course(request):
    #staffs = staff.objects.all()
    course=courses.objects.all()
    print(course)
    context = {
        # "staffs": staffs,
        "course":course
    }
    return render(request, 's1/manage_course_template.html', context)


def edit_course(request, id):
    # Adding Student ID into Session Variable
    request.session['id'] = id
    #print(id)
    course = courses.objects.get(course_id=id)
    context = {
        "course":course
    }
    return render(request, "s1/edit_course_template.html", context)


def edit_course_save(request,id):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        
        id = request.session.get('id')
        print(id)
        if id == None:
            return redirect('/manage_course')

        if request.method!="POST":
            return HttpResponse(request,"Method not allowed")
        else:
          course_id = request.POST.get('course_id')
          course_name=request.POST.get('course_name')
          dept=request.POST.get('dept')
            # First Update into Custom User Model
          try:
            course=courses.objects.get(course_id=course_id)
            course.Name=course_name
            course.dept=dept
            course.save()
            del request.session['id']  
            messages.success(request, "Course Updated Successfully!")       
          except:
            messages.success(request, "Failed to Update Course.")
          return redirect('manage_course')


def delete_course(request, course_id):
    course=courses.objects.get(course_id=course_id)
    try:
        course.delete()
        messages.success(request, "Course Deleted Successfully.")
    except:
        messages.error(request, "Failed to Delete Course.")
    return redirect('manage_course')


def add_class(request):
  course=courses.objects.all()
  if classes.objects.all().count()==0:
    clss=11
  else:
    clss=classes.objects.aggregate(max=Max("class_id"))["max"]+1
  context={
    "course":course,
    "clss":clss
  }
  return render(request,"s1/addclass.html",context)

def add_class_save(request):
  if request.method!="POST":
    return HttpResponse(request,"Method not allowd")
   
  else:
    cls=request.POST.get("name")
    cid=request.POST.get("class_id")
    cs=request.POST.get("course")
    course=courses.objects.get(course_id=cs)
    try:
      if classes.objects.filter(class_id=cid).exists():
        messages.error(request,"Failed to add Class!! Class ID already exists")
      elif classes.objects.filter(name=cls).exists():
        messages.error(request,"Failed to add Class!! Class already exists")
      else:
        classs_model=classes(class_id=cid,name=cls,course_id=course)
        classs_model.save()
        messages.success(request,"Successfuly added class")
    except:
      messages.error(request,"Failed to add class")
    return redirect("add_class")

def manage_class(request):
    #staffs = staff.objects.all()
    class1=classes.objects.all()
    print(class1)
    context = {
        # "staffs": staffs,
        "class1":class1
    }
    return render(request, 's1/manage_class_template.html', context)


def edit_class(request, id):
    # Adding Student ID into Session Variable
    request.session['id'] = id
    #print(id)
    class1 = classes.objects.get(class_id=id)
    course=courses.objects.all()
    context = {
        "class1":class1,
        "course":course
    }
    return render(request, "s1/edit_class_template.html", context)


def edit_class_save(request,id):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        
        id = request.session.get('id')
        print(id)
        if id == None:
            return redirect('/manage_class')

        if request.method!="POST":
            return HttpResponse(request,"Method not allowed")
        else:
          class_id = request.POST.get('class_id')
          class_name=request.POST.get('class_name')
          course_id=request.POST.get('course_id')
          try:
            class1=classes.objects.get(class_id=class_id)
            cid=courses.objects.get(course_id=course_id)
            class1.name=class_name
            class1.course_id=cid
            class1.save()
            del request.session['id']  
            messages.success(request, "Class Updated Successfully!")       
          except:
            messages.error(request, "Failed to Update Class.")
          return redirect('manage_class')


def delete_class(request, class_id):
    class1=classes.objects.get(class_id=class_id)
    try:
        class1.delete()
        messages.success(request, "Class Deleted Successfully.")
    except:
        messages.error(request, "Failed to Delete Class.")
    return redirect('manage_class')

def add_staff(request):
  course=courses.objects.all()
  if staff.objects.all().count()==0:
    stf=101
  else:
    stf=staff.objects.aggregate(max=Max("staff_id"))["max"]+1
  context={
    "course":course,
    "stf":stf
  }
  return render(request,"s1/addstaff.html",context)

def add_staff_save(request):
  if request.method!="POST":
    return HttpResponse(request,"Method not allowd")
  else:
    first_name = request.POST.get('staff_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    email = request.POST.get('email')
    pwd = request.POST.get('password')    
    sid=request.POST.get("staff_id")
    id=request.POST.get("course")
    sname = first_name+" "+last_name
    try:
      if staff.objects.filter(staff_id=sid).exists():
        messages.error(request,"Failed to add Staff!! Staff ID already exists")
      elif CustomUser.objects.filter(username=username).exists():
        messages.error(request,"Failed to add Staff!! Username already exists")
      elif CustomUser.objects.filter(email=email).exists():
        messages.error(request,"Failed to add Staff!! email ID already exists")
      else:
        user = CustomUser.objects.create_user(username=username, password=pwd, email=email, first_name=first_name, last_name=last_name, user_type=2)
        course=courses.objects.get(course_id=id)    
        user.staff.staff_id=sid
        user.staff.staff_name=sname
        user.staff.course_id=course
        user.save()
        messages.success(request,"Staff Added Successfully")
        return redirect("add_staff")
    except:
      messages.error(request,"Failed to add Staff")
    return redirect("addstaff")

def manage_staff(request):
    staffs = staff.objects.all()
    course=courses.objects.all()
    context = {
        "staffs": staffs,
        "course":course
    }
    return render(request, 's1/manage_staff_template.html', context)


def edit_staff(request, id):
    # Adding Student ID into Session Variable
    request.session['id'] = id
    #print(id)
    staffs = staff.objects.get(admin=id)
    s=staffs.staff_name
    first_name,last_name=s.split(" ")
    course=courses.objects.all()
    #print(cls)
    context = {
        'course':course,
        "id": id,
        "staffs":staffs,
        "first_name":first_name,
        "last_name":last_name,
        "username": staffs.admin.username,
    }
    return render(request, "s1/edit_staff_template.html", context)


def edit_staff_save(request,id):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        
        id = request.session.get('id')
        print(id)
        if id == None:
            return redirect('/manage_staff')

        if request.method!="POST":
            return HttpResponse(request,"Method not allowed")
        else:
          sid=request.POST.get('staff_id')
          email = request.POST.get('email')
          username = request.POST.get('username')
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          course_id = request.POST.get('course_id')
            # First Update into Custom User Model
          try:
              user = CustomUser.objects.get(id=id)
              user.first_name = first_name
              user.last_name = last_name
              user.email = email
              user.username = username
              user.save()
          
              course = courses.objects.get(course_id=course_id)
              print(course.course_id)

              staff1=staff.objects.get(admin=id)
              staff1.staff_id=sid
              staff1.staff_name=first_name+" "+last_name
              staff1.course=course.course_id
              staff1.save()
              del request.session['id']
              messages.success(request, "Staff Updated Successfully!")       
          except:
            messages.error(request, "Failed to Update Staff.")
          return redirect('manage_staff')


def delete_staff(request, staff_id):
    staffs = staff.objects.get(admin=staff_id)
    user = CustomUser.objects.get(id=staff_id)
    try:
        staffs.delete()
        user.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_staff')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_staff')






def add(request):
  course=courses.objects.all()
  cls=classes.objects.all()
  if stud.objects.all().count()==0:
    rn=20001 
  else:
    rn=stud.objects.aggregate(max=Max("rno"))["max"]+1
  context={
    'course':course,
    'cls':cls,
    'rn':rn
  }
  return render(request,'s1/addstudent.html',context)


def addrecord(request):
  if request.method!="POST":
    return HttpResponse(request,"Method not allowd")
  else:
    fn = request.POST.get('first_name')
    ln = request.POST.get('last_name')
    em=request.POST.get('email')
    un=request.POST.get('username')
    pwd=request.POST.get('password')
    rn = request.POST.get('rno') 
    gn=request.POST.get('gender')
    cl=request.POST.get('cls')
    sc=request.POST.get('sec')
    cs=request.POST.get('course')
    try:
      if stud.objects.filter(rno=rn).exists():
        messages.error(request,"Failed to add Student!! Roll Number already exists")
      elif CustomUser.objects.filter(username=un).exists():
        messages.error(request,"Failed to add Student!! Username already exists")
      elif CustomUser.objects.filter(email=em).exists():
        messages.error(request,"Failed to add Student!! email ID already exists")
      else:
        user = CustomUser.objects.create_user(username=un, password=pwd, email=em, first_name=fn, last_name=ln, user_type=3)
        user.stud.rno=rn
        user.stud.first_name=fn      
        user.stud.last_name=ln
        user.stud.sclass=cl
        user.stud.gender=gn
        user.stud.email=em
        user.stud.section=sc
        user.stud.course=cs
        user.save()
        messages.success(request,"Student Added Successfully")
        return redirect("add")
    except:
      messages.error(request,"Failed to add Student")
    return redirect("add")

    
def manage_student(request):
    students = stud.objects.all()
    course=courses.objects.all()
    context = {
        "students": students
    }
    return render(request, 's1/manage_student_template.html', context)


def edit_student(request, id):
    # Adding Student ID into Session Variable
    request.session['id'] = id
    #print(id)
    student = stud.objects.get(admin=id)
    #print(student.admin.id)
    course=courses.objects.all()
    cls=classes.objects.all()
    #print(cls)
    context = {
        "cls":cls,
        'course':course,
        "id": id,
        "student":student,
        "username": student.admin.username,
    }
    return render(request, "s1/edit_student_template.html", context)


def edit_student_save(request,id):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        
        id = request.session.get('id')
        print(id)
        if id == None:
            return redirect('/manage_student')

        if request.method!="POST":
            return HttpResponse(request,"Method not allowd")
        else:
          rn=request.POST.get('rno')
          email = request.POST.get('email')
          username = request.POST.get('username')
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          course_id = request.POST.get('course_id')
          gender = request.POST.get('gender')
          sclass=request.POST.get('cls')
          section=request.POST.get('section')
          print(section)

            # Getting Profile Pic first
            # First Check whether the file is selected or not
            # Upload only if file is selected
          
            # First Update into Custom User Model
          try:
            user = CustomUser.objects.get(id=id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
          
            course = courses.objects.get(course_id=course_id)
            print(course.course_id)

            stud1=stud.objects.get(admin=id)
            stud1.rno=rn
            stud1.first_name=first_name      
            stud1.last_name=last_name
            stud1.sclass=sclass
            stud1.gender=gender
            stud1.email=email
            stud1.section=section
            stud1.course=course.course_id
            stud1.save()
            del request.session['id']
            messages.success(request, "Student Updated Successfully!")       
          except:
            messages.error(request, "Failed to Update Student.")
          return redirect('manage_student')


def delete_student(request, student_id):
    student = stud.objects.get(admin=student_id)
    user = CustomUser.objects.get(id=student_id)
    try:
        student.delete()
        user.delete()
        messages.success(request, "Student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return redirect('manage_student')


def add_subject(request):
  staffs=staff.objects.all()
  cls=classes.objects.all()
  if subjects.objects.all().count()==0:
    sid=101
  else:
    sid=subjects.objects.aggregate(max=Max("subject_id"))["max"]+1
  context={
    'staffs':staffs,
    'cls':cls,
    'sid':sid
  }
  return render(request,'s1/addsubject.html',context)

def add_subject_save(request):
  if request.method!="POST":
    return HttpResponse(request,"Method not allowd")
   
  else:
    sname=request.POST.get("subject")
    subid=request.POST.get("subject_id")
    id=request.POST.get("staffs")
    staffs=staff.objects.get(staff_id=id)
    clid=request.POST.get("cls")
    cls=classes.objects.get(class_id=clid)
    try:
      if subjects.objects.filter(subject_id=subid).exists():
        messages.error(request,"Failed to add Subject!! Subject ID already exists")
      elif subjects.objects.filter(subject=sname).exists():
        messages.error(request,"Failed to add Subject!! Subject already exists")
      else:
        subject=subjects(subject_id=subid,subject=sname,class_id=cls,staff_id=staffs)
        subject.save()
        messages.success(request,"Successfuly added subject")
    except:
      messages.error(request,"Failed to add subject")
    return redirect("add_subject")

def manage_subject(request):
    subject=subjects.objects.all()
    context = {
        "subject":subject
    }
    return render(request, 's1/manage_subject_template.html', context)


def edit_subject(request, id):
    request.session['id'] = id
    subject = subjects.objects.get(subject_id=id)
    print(subject)
    course=courses.objects.all()
    class1=classes.objects.all()
    staffs=staff.objects.all()
    context = {
        "subject":subject,
        "course":course,
        "class1":class1,
        "staffs":staffs
    }
    return render(request, "s1/edit_subject_template.html", context)


def edit_subject_save(request,id):
    if request.method != "POST":
        return HttpResponse("Invalid Method!")
    else:
        
        id = request.session.get('id')
        print(id)
        if id == None:
            return redirect('/manage_subject')

        if request.method!="POST":
            return HttpResponse(request,"Method not allowed")
        else:
          subject_id = request.POST.get('subject_id')
          subject_name=request.POST.get('subject_name')
          class_id=request.POST.get('class_id')
          staff_id=request.POST.get('staff_id')
          try:
            subject=subjects.objects.get(subject_id=subject_id)
            cid=classes.objects.get(class_id=class_id)
            sid=staff.objects.get(staff_id=staff_id)
            subject.subject=subject_name
            subject.class_id=cid
            subject.staff_id=sid
            subject.save()
            del request.session['id']  
            messages.success(request, "Subject Updated Successfully!")       
          except:
            messages.error(request, "Failed to Update Subject.")
          return redirect('manage_subject')


def delete_subject(request, subject_id):
    subject=subjects.objects.get(subject_id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
    except:
        messages.error(request, "Failed to Delete Subject.")
    return redirect('manage_subject')

def take_attendance(request):
  cls=classes.objects.all()
  context={
    'cls':cls
  }
  return render(request,"s1/takeattendance.html",context)

def attend(request):
  subject=subjects.objects.all()
  clss=request.POST.get("cls")
  sect=request.POST.get("section")
  student=stud.objects.filter(sclass=clss,section=sect)
  context={
    "subject":subject,
    "student":student
  }
  return render(request,"s1/attendancesave.html",context)

def attendance_save(request):
  sub=request.POST.get("subject")
  subject=subjects.objects.get(subject_id=sub)
  print(subject)
  date=request.POST.get("date")
  studs=request.POST.get("student")
  print(studs)
  student=stud.objects.get(rno=studs)
  try:
    if 'present' in request.POST:
      attend=attendance(rid=student,rno=student.rno,subject_id=subject,attendance_date=date,status=0)
      attend.save()
      messages.success(request,"Successffully added attendance")
    elif 'absent' in request.POST:
      attend=attendance(rid=student,rno=student.rno,subject_id=subject,attendance_date=date,status=1)
      attend.save()
      messages.success(request,"Successfully added attendance")
  except:
    messages.error(request,"give appropriate details")
  return HttpResponseRedirect("attend")

   
def add_aadvisor(request):   
    cls=classes.objects.all() 
    staffs=staff.objects.all() 
    context={  
    'cls':cls,
    'staffs':staffs,
  }
    return render(request,"s1/addacademicadvisor.html",context)

def add_aadvisor_save(request): 
  if request.method!="POST":
    return HttpResponse(request,"Method not allowd")
  else:
    clss=request.POST.get("cls")
    sec=request.POST.get("sec")
    student=stud.objects.filter(sclass=clss,section=sec)
    stf=request.POST.get("staffs")
    staffs=staff.objects.get(staff_id=stf)
    stfs=staffs.staff_name 
    try:
      if stud.objects.filter(sclass=clss,academic_advisor=stfs).exists():
        messages.error(request,"Academic advisor is already assigned to this class")
      else:
        for s in student:
          studData=s.rno
          students=stud.objects.get(rno=studData)
          students.academic_advisor=stfs
          students.save()
        messages.success(request,"Successfully added")
    except:
      messages.error(request,"Class have no students")
    return redirect("addacademicadvisor")

#leave_application
def student_apply_leave(request):
    student_obj = stud.objects.get(admin=request.user.id)
    leave_data = leave.objects.filter(id=student_obj)
    print(leave_data)
    staffs=staff.objects.get(staff_name=student_obj.academic_advisor)
    print(staffs)
    context = {
        "staffs": staffs,
        "leave_data": leave_data
    }
    return render(request, 's1/student_apply_leave.html', context)
    
def student_apply_leave_save(request):
    if request.method == "POST":
      student_obj = stud.objects.get(admin=request.user.id)
      rno=student_obj.rno
      leave_date = request.POST.get('leave_date')
      leave_reason = request.POST.get('leave_reason')
      staffs=staff.objects.get(staff_name=student_obj.academic_advisor)
      try:       
        leave_report = leave(id=student_obj,rno=rno,staff_id=staffs.staff_id,leave_reason=leave_reason, leave_date=leave_date, leave_status=0)
        print(leave_report)
        leave_report.save()
        messages.success(request, 'Applied for Leave.')
        #return render(request, 's1/student_apply_leave.html')
        return redirect('student_apply_leave')
      except:
        messages.error(request, 'Failed to Apply Leave')
        return redirect('student_apply_leave')
      
    else:
      return redirect('student_apply_leave')
    messages.error(request, "Invalid Method")
            

def staff_leave_view(request):
    #leaves = leave.objects.all()
    staff_obj=staff.objects.get(admin=request.user.id)
    s1=staff_obj.staff_id
    leaves=leave.objects.filter(staff_id=s1)
    print(leaves)
    context = {
        "leaves": leaves
    }
    return render(request, 's1/leave_view.html', context)

def staff_leave_approve(request, leave_id):
    leav = leave.objects.get(leave_id=leave_id)
    leav.leave_status = 1
    leav.save()
    return redirect(reverse(staff_leave_view))


def staff_leave_reject(request, leave_id):
    leav = leave.objects.get(leave_id=leave_id)
    leav.leave_status = 2
    leav.save()
    return redirect(reverse('staff_leave_view'))

@csrf_exempt
def student_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        student=stud.objects.get(admin=request.user.id)
        student.fcm_token=token
        student.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def admin_send_notification_student(request):
    student=stud.objects.all()
    return render(request,"s1/student_notification.html",{"student":student})

def add_parent(request):
  # stud1=stud.objects.all()
  if parent.objects.all().count()==0:
    ptr=1
  else:
    ptr=parent.objects.aggregate(max=Max("parent_id"))["max"]+1
  context={
    # "stud1":stud1,
    "ptr":ptr
    
  }
  return render(request,"s1/parent_register.html",context)

def add_parent_save(request):
  if request.method!="POST":
    return HttpResponse(request,"Method not allowd")
  else:
    try:
      first_name = request.POST.get('parent_name')
      last_name = request.POST.get('last_name')
      username = request.POST.get('username')
      email = request.POST.get('email')
      pwd = request.POST.get('password')    
      pid=request.POST.get("parent_id")
      contact = request.POST.get('contact') 
      id=request.POST.get("rno")
      sid=stud.objects.get(rno=id)
      pname = request.POST.get('parent_name')
      user = CustomUser.objects.create_user(username=username, password=pwd, email=email, first_name=first_name, last_name=last_name, user_type=4)
      stud1=stud.objects.get(rno=id)    
      user.parent.parent_id=pid
      user.parent.parent_name=pname
      user.parent.rno=stud1
      user.parent.contact=contact
      user.save()
      messages.success(request,"Successfuly added parent")
    except:
      messages.error(request,"Failed to add parent")
    return HttpResponseRedirect("add_parent")



def student_mark(request):
  cls=classes.objects.all()
  context={
    'cls':cls
  }
  return render(request,"s1/mark.html",context)

def student_mark_save(request):
  subject=subjects.objects.all()
  clid=request.POST.get("cls")
  print(clid)
  sect=request.POST.get("sec")
  print(sect)
  sts=stud.objects.filter(sclass=clid,section=sect)
  context={
    "subject":subject,
    "sts":sts
  }
  return render(request,"s1/marksave.html",context)

def mark_report(request):
  if request.method!="POST":
    return HttpResponse(request,"Method not allowd")
  else:
    sub=request.POST.get("subject")
    subject=subjects.objects.get(subject_id=sub)
    cat=request.POST.get("category")
    mrk=request.POST.get("mark")
    st=request.POST.get("sts")
    student=stud.objects.get(rno=st)
    try:
      if mark.objects.filter(rno=student.rno,subject_id=subject,category=cat).exists():
        messages.error(request,"Failed to add mark!!  Mark already assigned")
      else:
        marks=mark(mid=student,rno=student.rno,subject_id=subject,marks=mrk,category=cat)
        marks.save()
        messages.success(request,"Mark added successfully")
    except:
      messages.error(request,"Failed to add mark")
    return redirect("student_mark_save")

# midday_meal application
def midday_meal(request):
  student_obj = stud.objects.get(admin=request.user.id)
  m_data = application.objects.filter(id=student_obj)
  context = {
    "m_data": m_data
  }
  return render(request, 's1/midday_meal_apply.html',context)

def midday_meal_save(request):
  if request.method != "POST":
    return redirect('midday_meal')
    messages.error(request, "Invalid Method")
  else:
    #rno = request.POST.get('rno')
    distance = request.POST.get('distance')
    income_status = request.POST.get('income_status')
    student_obj = stud.objects.get(admin=request.user.id)
    rno=student_obj.rno
    try:
      if application.objects.filter(rno=rno).exists():
        messages.error(request,"Only one application can be applied")
      else:
        m=application(id=student_obj,rno=student_obj.rno,distance=distance,income_status=income_status,appn_status=0)
        print(m)
        m.save()
        messages.success(request, 'Applied for Midday Meal.')
      return redirect('midday_meal')
    except:
      messages.error(request, 'Failed to Midday Meal')
      return redirect('midday_meal')

def midday_meal_view(request):
  meals = application.objects.all()
  print(meals)
  context = {
    "meals": meals
  }
  return render(request, 's1/view_midday_meal.html',context)

def midday_meal_approve(request,appn_id):
    meals = application.objects.get(appn_id=appn_id)
    meals.appn_status = 1
    meals.save()
    return redirect(reverse(midday_meal_view)) 

def midday_meal_reject(request,appn_id):
    meals = application.objects.get(appn_id=appn_id)
    meals.appn_status = 2
    meals.save()
    return redirect(reverse(midday_meal_view)) 


def scholarship(request):
  return render(request,"s1/scholarship.html")

def scholarship_save(request):
  cat=request.POST.get("category")
  m= mark.objects.values('rno').filter(category=cat)

  k=m.values_list('subject_id')
  #print(k)
  n=m.annotate(s=Count('subject_id',distinct=True))
  print(n.values_list('rno','s'))
  v=n.values_list('s')
  #print(v[rno])
  mks = mark.objects.values('rno').filter(category=cat).annotate(marks=(Sum('marks')/v[0]))

  rn=mark.objects.all()
  context = {
        'rn' : rn,
        'mks' : mks
    }
  rno=mks.values_list('rno','marks')
  print(rno)
  for i,j in rno:
     if cat=="First Internal" or "Second Internal":
        if j>=95.0:
          stud1=stud.objects.get(rno=i)
          stud1.scholarship="assigned"
          stud1.save()
        else:
          stud1=stud.objects.get(rno=i)
          stud1.scholarship="Not eligible"
          stud1.save()
     else:
        if j>=95:
          stud1=stud.objects.get(rno=i)
          stud1.scholarship="assigned"
          stud1.save()
        else:
          stud1=stud.objects.get(rno=i)
          stud1.scholarship="Not eligible"
          stud1.save()
  return render(request,"s1/scholarshipassign.html",context)

def per_info(request):
  st=stud.objects.get(admin=request.user.id)
  context={
    'st':st
  }
  return render(request,'s1/personalinfo.html',context)

def pinfo(request):
  try:
    rn = request.POST['rno']
    pic = request.FILES['profile']
    fname=request.POST['fname']
    mname=request.POST['mname']
    cno=request.POST['cno']
    addr=request.POST['addr']
    dob=request.POST['dob']
    ach=request.POST['achievements']
    stud1=stud.objects.get(rno=rn)
    stud1.rno=rn
    stud1.profile_pic=pic
    stud1.father_name=fname
    stud1.mother_name=mname
    stud1.contact=cno
    stud1.address=addr
    stud1.DOB=dob
    stud1.achievements=ach
 # stud1 = stud(rno=rno,father_name=fname, mother_name=mname, contact=cno,address=addr,DOB=dob )
    stud1.save()
    messages.success(request, 'Successfully added information')
  except:
    messages.error(request, 'Failed to add information!')
  return HttpResponseRedirect(reverse('per_info'))  

  

def email_send(request):
  if request.method=="POST":
    sub = request.POST.get('Subject')
    msg = request.POST.get('message')
    #from_email = settings.EMAIL_HOST_USER
    email = request.POST.get('email')
    to_list=[email]
    print(sub,msg,to_list)
    send_mail(
      sub,msg,'chaithrika2001@gmail.com',to_list,fail_silently = True
    )
    messages.success(request, 'Successfully added information')
  return render(request, 's1/sending_mail.html')

#query
def parent_query(request):
  parent_obj = parent.objects.get(admin=request.user.id)
  staffs=staff.objects.get(staff_name=parent_obj.rno.academic_advisor)
  print(staffs)
  query_data = query.objects.filter(parent_id=parent_obj)
  context = {
      "staffs":staffs,
      "query_data": query_data
  }
  return render(request, 's1/parent_query.html', context)

def parent_query_save(request):
  if request.method != "POST":
    messages.error(request, "Invalid Method.")
    return redirect('parent_query')
  else:
    querys = request.POST.get('query_msg')
    parent_obj = parent.objects.get(admin=request.user.id)
    s=parent_obj.rno.academic_advisor
    staffs=staff.objects.get(staff_name=s)
    print(staffs.staff_id)
    try:
      add_query = query(parent_id=parent_obj,staff_id=staffs.staff_id, querys=querys, query_reply="")
      add_query.save()
      messages.success(request, "Query Sent.")
      return redirect('parent_query')
    except:
      messages.error(request, "Failed to send query.")
      return redirect('parent_query')

def parent_query_message(request):
    staff_obj=staff.objects.get(admin=request.user.id)
    s1=staff_obj.staff_id
    query1=query.objects.filter(staff_id=s1)
    context={
      "query1":query1
    }
    return render(request,"s1/parent_query_reply.html",context)


@csrf_exempt
def parent_query_message_reply(request):
    query_id = request.POST.get('id')
    query_reply = request.POST.get('reply')
    staff_obj=staff.objects.get(admin=request.user.id)
    s1=staff_obj.staff_id
    stf=staff.objects.get(staff_id=s1)
    #student_obj = stud.objects.get(admin=request.user.id)
    try:
        query1 = query.objects.get(id=query_id,staff_id=stf.staff_id)
        query1.query_reply = query_reply
        query1.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

#Student_notification
def featch_student(request):
  cls=classes.objects.all()
  context={
    'cls':cls
  }
  return render(request,"s1/featch_student.html",context)

def staff_notification(request):
  staff_obj = staff.objects.get(admin=request.user.id)
  clss=request.POST.get("cls")
  sect=request.POST.get("section")
  student=stud.objects.filter(sclass=clss,section=sect)
  notification_data = notification.objects.filter(staff_id=staff_obj.staff_id)
  context = {
      "student":student,
      "notification_data": notification_data
  }
  return render(request, 's1/notifications.html', context)

def staff_notification_save(request):
  if request.method != "POST":
    messages.error(request, "Invalid Method.")
    return redirect('staff_notification')
  else:
    student_id=request.POST.get('student')
    stud1=stud.objects.get(rno=student_id)
    notifications = request.POST.get('notification_msg')
    staff_obj = staff.objects.get(admin=request.user.id)
    staff_id=staff_obj.staff_id
    staff_name=staff_obj.staff_name
    try:
        add_notification = notification(student_id=stud1.rno,messages=notifications,staff_id=staff_id,staff_name=staff_name)
        add_notification.save()
        messages.success(request, "notification Sent.")
        return redirect('staff_notification')
    except:
        messages.error(request, "Failed to Send notification.")
        return redirect('staff_notification')

def staff_notification_message(request):
    student_obj=stud.objects.get(admin=request.user.id)
    student_id=student_obj.rno
    notification1=notification.objects.filter(student_id=student_id)
    context={
      "notification1":notification1
    }
    return render(request,"s1/notification_view.html",context)

#Parent_notification
def staff_parent_notifications(request):
  clss=classes.objects.all()
  context = {
      "clss":clss
  }
  return render(request, 's1/fetch_parents.html', context)

def staff_parent_notification(request):
  staff_obj = staff.objects.get(admin=request.user.id)
  notification_data = notification.objects.filter(staff_id=staff_obj.staff_id)
  parents=parent.objects.all()
  print(parents)
  context = {
      "notification_data": notification_data,
      "parents":parents
  }
  return render(request, 's1/parent_notification.html', context)
  
def staff_notification_parent__save(request):
  if request.method != "POST":
    messages.error(request, "Invalid Method.")
    return redirect('staff_parent_notification')
  else:
    parent_id=request.POST.get('parent_id')
    parent1=parent.objects.get(parent_id=parent_id)
    notifications = request.POST.get('notification_msg')
    staff_obj = staff.objects.get(admin=request.user.id)
    staff_id=staff_obj.staff_id
    staff_name=staff_obj.staff_name
    try:
        add_notification = notification(parent_id=parent1.parent_id,parent_message=notifications,staff_id=staff_id,staff_name=staff_name)
        add_notification.save()
        messages.success(request, "notification Sent.")
        return redirect('staff_parent_notification')
    except:
        messages.error(request, "Failed to Send notification.")
        return redirect('staff_parent_notification')

def staff_parent_notification_message(request):
    parent_obj=parent.objects.get(admin=request.user.id)
    parent_id=parent_obj.parent_id
    notification1=notification.objects.filter(parent_id=parent_id)
    context={
      "notification1":notification1
    }
    return render(request,"s1/parent_notification_view.html",context)


# feedback
def student_feedback(request):
  student_obj = stud.objects.get(admin=request.user.id)
  staffs=staff.objects.get(staff_name=student_obj.academic_advisor)
  feedback_data = feedback.objects.filter(student_id=student_obj)
  context = {
      "staffs":staffs,
      "feedback_data": feedback_data
  }
  return render(request, 's1/student_feedback.html', context)

def student_feedback_save(request):
  if request.method != "POST":
    messages.error(request, "Invalid Method.")
    return redirect('student_feedback')
  else:
    feedbacks = request.POST.get('feedback_msg')
    student_obj = stud.objects.get(admin=request.user.id)
    s=student_obj.academic_advisor
    staffs=staff.objects.get(staff_name=s)
    try:
      add_feedback = feedback(student_id=student_obj,staff_id=staffs.staff_id, feedbacks=feedbacks, feedback_reply="")
      add_feedback.save()
      messages.success(request, "feedback Sent.")
      return redirect('student_feedback')
    except:
      messages.error(request, "Failed to Send Feedback.")
      return redirect('student_feedback')

  
def student_feedback_message(request):
    staff_obj=staff.objects.get(admin=request.user.id)
    s1=staff_obj.staff_id
    feedback1=feedback.objects.filter(staff_id=s1)
    context={
      "feedback1":feedback1
    }
    return render(request,"s1/student_feedback_reply.html",context)


@csrf_exempt
def student_feedback_message_reply(request):
    feedback_id = request.POST.get('id')
    feedback_reply = request.POST.get('reply')
    staff_obj=staff.objects.get(admin=request.user.id)
    s1=staff_obj.staff_id
    stf=staff.objects.get(staff_id=s1)
    #student_obj = stud.objects.get(admin=request.user.id)
    
    try:
        feedback1 = feedback.objects.get(id=feedback_id,staff_id=stf.staff_id)
        feedback1.feedback_reply = feedback_reply
        feedback1.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")

def mark_view(request):
  student_obj=stud.objects.get(admin=request.user.id)
  st1=student_obj.rno
  sname=student_obj.first_name
  students=mark.objects.filter(rno=st1)
  context={
    "students":students,
    "sname":sname
  }
  return render(request,'s1/viewmark.html',context)

def student_view(request):
  student_obj=stud.objects.get(admin=request.user.id)
  st1=student_obj.rno
  sname=student_obj.first_name
  lname=student_obj.last_name
  students=stud.objects.filter(rno=st1)
  context={
    "students":students,
    "sname":sname,
    "lname":lname
  }
  return render(request,'s1/studentview.html',context)

#shortage
def shortage(request):
  cls=classes.objects.all()
  subject=subjects.objects.all()
  context={
    "subject":subject,
    'cls':cls
  }
  return render(request,"s1/shortage.html",context)

def shortage_calc(request):
  if request.method!="POST":
    return HttpResponse(request,"Method not allowd")
  else:
    sclass=request.POST.get("cls")
    sec=request.POST.get("sec")
    subject=request.POST.get("subject")
    date1=request.POST.get("date1")
    date2=request.POST.get("date2")
    att=attendance.objects.all()
    a=attendance.objects.filter(subject_id=subject)
    b=a.filter(attendance_date__lte=date2,attendance_date__gte=date1).values('attendance_date').distinct()
    class_held=b.count()
    print(class_held)
    a1 = attendance.objects.values('rno','status').filter(attendance_date__lte=date2,attendance_date__gte=date1,subject_id=subject)
    dic={} 
    for dis in a1: 
      if(dis['rno'] in dic): 
        if(dis['status']==0):         
            dic[dis['rno']]+=1 
      else: 
        dic[dis['rno']]=0 
        if(dis['status']==0):         
            dic[dis['rno']]+=1 
    print(dic)
    for x,y in dic.items():
      d={}
      class_attended=0
      sp=(y/class_held)*100
      print(sp)
      if(sp<75):
        d[x]=sp
        class_attended=y 
    print(dic)
    print(d)
    context={
    "dic":dic,
    "d":d,
    "sclass":sclass,
    "sec":sec,
    "class_attended":class_attended,
    "class_held":class_held
    }
  return render(request,"s1/shortage_view.html",context)

def parent_view(request):
  parent_obj=parent.objects.get(admin=request.user.id)
  st1=parent_obj.rno
  st=st1.rno
  sname=parent_obj.parent_name
  students=stud.objects.filter(rno=st)
  context={
    "students":students,
    "sname":sname,
  }
  return render(request,'s1/studentview.html',context)

def mark_parent_view(request):
  parent_obj=parent.objects.get(admin=request.user.id)
  st1=parent_obj.rno
  st=st1.rno
  students=mark.objects.filter(rno=st)
  context={
    "students":students,
  }
  return render(request,'s1/viewmark.html',context)