from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..models import *


@login_required(login_url='/')
def student_home(request):
    error = ''
    context = {}
    student = Student(request.user.username)
    if request.method == 'POST':
        data = request.POST
        try:
            name = data['name']
            if name == '':
                name = None
            year = data['year']
            if year == '':
                year = None
            program_name = data['program']
            if program_name == '':
                prog_id = None
            else:
                prog = Program(program_name)
                prog.fill()
                prog_id = prog.prog_id
            dept_name = data['department']
            if dept_name == '':
                dept_id = None
            else:
                department = Department(dept_name)
                department.fill()
                dept_id = department.dept_id
            student.update(name, year, prog_id, dept_id)
        except:
            error = 'DB error'
    
    context['error'] = error
    student.fill()
    
    context['student_data'] = [student.name, student.year, student.prog_name, student.dept_name]
    return render(request, 'student/home.html', context)


@login_required(login_url='/')
def student_test(request):
    return render(request, 'student/test.html')