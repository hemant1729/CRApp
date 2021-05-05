from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from ..models import *


def is_admin(user):
    return user.is_authenticated and user.username=='admin'


@user_passes_test(is_admin)
def admin_home(request):
    return render(request, 'admin/home.html')


@user_passes_test(is_admin)
def admin_program(request):
    error = ''
    context = {}
    if request.method == 'POST': 
        data = request.POST
        try:
            if 'add' in data:
                prog_name = data['prog_name']
                prog = Program(prog_name=prog_name)
                prog.insert()
            elif 'search' in data:
                prog_name = data['prog_name']
                prog_list = Program.search(prog_name)
                prog_names = [p.prog_name for p in prog_list]
                context['prog_names'] = prog_names
            elif 'update' in data:
                #delete has more priority 
                for d in data.getlist('delete_list'):
                    prog = Program(d)
                    prog.delete()
                for u in data.getlist('update_list'):
                    uid, uname = u.split(':')
                    if uname in data.getlist('delete_list'):
                        continue
                    prog = Program(prog_name=uname)
                    prog.update(data.getlist('updated_names')[int(uid)])

        except:
            error = 'DB error'

    context['error'] = error 
    return render(request, 'admin/program.html', context)


@user_passes_test(is_admin)
def admin_dept(request):
    error = ''
    context = {}
    if request.method == 'POST': 
        data = request.POST
        try:
            if 'add' in data:
                dept_name = data['dept_name']
                dept = Department(dept_name=dept_name)
                dept.insert()
            elif 'search' in data:
                dept_name = data['dept_name']
                dept_list = Department.search(dept_name)
                dept_names = [d.dept_name for d in dept_list]
                context['dept_names'] = dept_names
            elif 'update' in data:
                #delete has more priority 
                for d in data.getlist('delete_list'):
                    dept = Department(d)
                    dept.delete()
                for u in data.getlist('update_list'):
                    uid, uname = u.split(':')
                    if uname in data.getlist('delete_list'):
                        continue
                    dept = Department(dept_name=uname)
                    dept.update(data.getlist('updated_names')[int(uid)])

        except:
            error = 'DB error'

    context['error'] = error 
    return render(request, 'admin/dept.html', context)


@user_passes_test(is_admin)
def admin_course(request):
    error = ''
    context = {}
    if request.method == 'POST': 
        data = request.POST
        try:
            if 'add' in data:
                course_name = data['course_name']
                dept_name = data['dept_name']
                dept = Department(dept_name=dept_name)
                dept.insert()
            elif 'search' in data:
                dept_name = data['dept_name']
                dept_list = Department.search(dept_name)
                dept_names = [d.dept_name for d in dept_list]
                context['dept_names'] = dept_names
            elif 'update' in data:
                #delete has more priority 
                for d in data.getlist('delete_list'):
                    dept = Department(d)
                    dept.delete()
                for u in data.getlist('update_list'):
                    uid, uname = u.split(':')
                    if uname in data.getlist('delete_list'):
                        continue
                    dept = Department(dept_name=uname)
                    dept.update(data.getlist('updated_names')[int(uid)])

        except:
            error = 'DB error'

    context['error'] = error 
    return render(request, 'admin/course.html', context)

@user_passes_test(is_admin)
def admin_test(request):
    return render(request, 'admin/test.html')