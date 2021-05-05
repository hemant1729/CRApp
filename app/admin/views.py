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
@user_passes_test(is_admin)
def admin_tags(request):
    error = ''
    context = {}
    if request.method == 'POST': 
        data = request.POST
        try:
            if 'add' in data:
                tag_name = data['tag_name']
                tag = Tag(tag_name=tag_name)
                tag.insert()
            elif 'search' in data:
                tag_name = data['tag_name']
                tag_list = Tag.search(tag_name)
                tag_names = [d.tag_name for d in tag_list]
                context['tag_names'] = tag_names
            elif 'update' in data:
                #delete has more priority 
                for d in data.getlist('delete_list'):
                    tag = Tag(d)
                    tag.delete()
                for u in data.getlist('update_list'):
                    uid, uname = u.split(':')
                    if uname in data.getlist('delete_list'):
                        continue
                    tag = Tag(tag_name=uname)
                    tag.update(data.getlist('updated_names')[int(uid)])

        except:
            error = 'DB error'

    context['error'] = error 
    return render(request, 'admin/tags.html', context)

@user_passes_test(is_admin)
def admin_course_tags(request):
    if request.GET.get('course_id'):
        error = ''
        context = {}
        try:
            course_tag = Course_tags(request.GET['course_id'])
            tag_list = course_tag.get_tags()
            tag_names = [d.tag_name for d in tag_list]
            context['course_tag_names'] = tag_names
            context['course_name'] = course_tag.get_name()
            context['course_id'] = request.GET['course_id']
        except:
            error = 'DB error'
        context['error'] = error
        return render(request, 'admin/course_tags.html', context)
    error = ''
    context = {}
    if request.method == 'POST':
        data = request.POST
        print(data)
        try:
            context['course_name'] = data['course_name']
            context['course_id'] = data['course_id']
            if 'search' in data:
                tag_name = data['tag_name']
                tag_list = Tag.search(tag_name)
                tag_names = [d.tag_name for d in tag_list]
                context['tag_names'] = tag_names
            elif 'update' in data:
                course_id = data['course_id']
                course_tag = Course_tags(course_id)
                for d in data.getlist('delete_list'):
                    course_tag.remove_tag(d)
                for a in data.getlist('add_list'):
                    course_tag.add_tag(a)
            course_tag = Course_tags(data['course_id'])
            tag_list = course_tag.get_tags()
            tag_names = [d.tag_name for d in tag_list]
            context['course_tag_names'] = tag_names
        except:
            error = 'DB error'

    context['error'] = error 
    return render(request, 'admin/course_tags.html', context)
