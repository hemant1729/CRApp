from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..models import *
from ..recommender.models import *

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

@login_required(login_url='/')
def student_interests(request):
    student = Student(request.user.username)
    student.fill()
    if request.method == 'GET':
        error = ''
        context = {}
        try:
            interests = Interests(student.student_id)
            tag_list = interests.get_tags()
            tag_names = [d.tag_name for d in tag_list]
            context['student_tag_names'] = tag_names
        except:
            error = 'DB error'
        context['error'] = error
        return render(request, 'student/interests.html', context)
    error = ''
    context = {}
    if request.method == 'POST':
        data = request.POST
        try:
            if 'search' in data:
                tag_name = data['tag_name']
                tag_list = Tag.search(tag_name)
                tag_names = [d.tag_name for d in tag_list]
                context['tag_names'] = tag_names
            elif 'update' in data:
                interests = Interests(student.student_id)
                for d in data.getlist('delete_list'):
                    interests.remove_tag(d)
                for a in data.getlist('add_list'):
                    interests.add_tag(a)
            interests = Interests(student.student_id)
            tag_list = interests.get_tags()
            tag_names = [d.tag_name for d in tag_list]
            context['student_tag_names'] = tag_names
        except:
            error = 'DB error'
    context['error'] = error 
    return render(request, 'student/interests.html', context)
