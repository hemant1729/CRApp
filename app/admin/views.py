from django.shortcuts import render, redirect
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
                credits = data['credits']
                dept = Department(dept_name=dept_name)
                dept.fill()
                course = Course(course_name, dept.dept_id, credits)
                course.insert()
            elif 'search' in data:
                course_name = data['course_name']
                dept_name = data['dept_name']
                course_list = Course.search(course_name, dept_name)
                course_names = [[c.course_name, '' if c.dept_name is None else c.dept_name, '' if c.credits is None else c.credits, c.course_id] for c in course_list]
                context['course_names'] = course_names
            elif 'update' in data:
                #delete has more priority 
                for c in data.getlist('delete_list'):
                    course = Course(course_name=c)
                    course.delete()

                for u in data.getlist('update_list'):
                    uid, uname = u.split(':')
                    if uname in data.getlist('delete_list'):
                        continue
                    course = Course(course_name=uname)
                    new_course_name = data.getlist('updated_course_names')[int(uid)]

                    new_dept_name = data.getlist('updated_dept_names')[int(uid)]
                    if new_dept_name != '':
                        new_dept = Department(dept_name=new_dept_name)
                        new_dept.fill()
                        new_dept_id = new_dept.dept_id
                    else:
                        new_dept_id = None

                    new_credits = data.getlist('updated_credits')[int(uid)]
                    new_credits = None if new_credits == '' else new_credits

                    course.update(new_course_name, new_dept_id, new_credits)

        except:
            error = 'DB error'

    context['error'] = error 
    return render(request, 'admin/course.html', context)


@user_passes_test(is_admin)
def admin_instr(request):
    error = ''
    context = {}
    if request.method == 'POST': 
        data = request.POST
        try:
            if 'add' in data:
                roll_num = data['roll_num']
                instr_name = data['instr_name']
                dept_name = data['dept_name']
                dept = Department(dept_name=dept_name)
                dept.fill()
                instr = Instructor(roll_num, instr_name, dept.dept_id)
                instr.insert()
            elif 'search' in data:
                roll_num = data['roll_num']
                instr_name = data['instr_name']
                dept_name = data['dept_name']
                instr_list = Instructor.search(roll_num, instr_name, dept_name)
                instr_names = [[i.roll_num, i.instr_name, '' if i.dept_name is None else i.dept_name] for i in instr_list]
                context['instr_names'] = instr_names
            elif 'update' in data:
                #delete has more priority 
                for r in data.getlist('delete_list'):
                    instr = Instructor(roll_num=r)
                    instr.delete()

                for u in data.getlist('update_list'):
                    uid, uname = u.split(':')
                    if uname in data.getlist('delete_list'):
                        continue
                    instr = Instructor(roll_num=uname)
                    new_roll_num = data.getlist('updated_roll_nums')[int(uid)]
                    new_instr_name = data.getlist('updated_instr_names')[int(uid)]
                    new_dept_name = data.getlist('updated_dept_names')[int(uid)]
                    if new_dept_name != '':
                        new_dept = Department(dept_name=new_dept_name)
                        new_dept.fill()
                        new_dept_id = new_dept.dept_id
                    else:
                        new_dept_id = None

                    instr.update(new_roll_num, new_instr_name, new_dept_id)

        except:
            error = 'DB error'

    context['error'] = error 
    return render(request, 'admin/instr.html', context)


@user_passes_test(is_admin)
def admin_sem(request):
    error = ''
    context = {}
    if request.method == 'POST': 
        data = request.POST
        try:
            if 'add' in data:
                year = data['year']
                season = data['season']
                sem = Semester(year, season)
                sem.insert()
            elif 'search' in data:
                year = data['year']
                season = data['season']
                sem_list = Semester.search(year, season)
                sem_names = [[s.year, s.season] for s in sem_list]
                context['sem_names'] = sem_names
            elif 'update' in data:
                #delete has more priority 
                for s in data.getlist('delete_list'):
                    s = s.split(':')
                    sem = Semester(year=s[0], season=s[1])
                    sem.delete()

                for u in data.getlist('update_list'):
                    uid, uyear, useason = u.split(':')
                    if uyear+':'+useason in data.getlist('delete_list'):
                        continue
                    sem = Semester(year=uyear, season=useason)
                    new_year = data.getlist('updated_years')[int(uid)]
                    new_season = data.getlist('updated_seasons')[int(uid)]

                    sem.update(new_year, new_season)

        except:
            error = 'DB error'

    context['error'] = error 
    return render(request, 'admin/sem.html', context)


@user_passes_test(is_admin)
def admin_timeslot(request):
    error = ''
    context = {}
    if request.method == 'POST': 
        data = request.POST
        try:
            if 'add' in data:
                time_slot_id = data['time_slot_id']
                day = data['day']
                start_time = data['start_time']
                end_time = data['end_time']
                timeslot = Timeslot(time_slot_id, day, start_time, end_time)
                timeslot.insert()
            elif 'search' in data:
                time_slot_id = data['time_slot_id']
                day = data['day']
                start_time = data['start_time']
                end_time = data['end_time']
                timeslots = Timeslot.search(time_slot_id, day, start_time, end_time)
                timeslot_names = [[t.time_slot_id, t.day, t.start_time, t.end_time] for t in timeslots]
                context['timeslot_names'] = timeslot_names
            elif 'update' in data:
                #delete has more priority 
                for s in data.getlist('delete_list'):
                    s=s[1:-1]
                    s=s.split(', ')
                    s=[si[1:-1] for si in s]
                    timeslot = Timeslot(s[0], s[1], s[2], s[3])
                    timeslot.delete()

                for u in data.getlist('update_list'):
                    u = u.split(':', 1)
                    uid = u[0]
                    uarray = u[1]
                    if uarray in data.getlist('delete_list'):
                        continue

                    uarray = uarray[1:-1]
                    uarray = uarray.split(', ')
                    uarray = [ui[1:-1] for ui in uarray]

                    timeslot = Timeslot(uarray[0], uarray[1], uarray[2], uarray[3])
                    new_time_slot_id = data.getlist('updated_time_slot_ids')[int(uid)]
                    new_day = data.getlist('updated_days')[int(uid)]
                    new_start_time = data.getlist('updated_start_times')[int(uid)]
                    new_end_time = data.getlist('updated_end_times')[int(uid)]

                    timeslot.update(new_time_slot_id, new_day, new_start_time, new_end_time)

        except:
            error = 'DB error'

    context['error'] = error 
    return render(request, 'admin/timeslot.html', context)


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


@user_passes_test(is_admin)
def admin_course_sem(request):
    error = ''
    context = {}
    if request.method == 'POST': 
        data = request.POST
        try:
            if 'add' in data:
                course_name = data['course_name']
                course = Course(course_name=course_name)
                course.fill()
                course_id = course.course_id

                sem_year = data['sem_year']
                sem_season = data['sem_season']
                sem = Semester(sem_year, sem_season)
                sem.fill()
                sem_id = sem.sem_id

                roll_num = data['roll_num']
                instructor = Instructor(roll_num=roll_num)
                instructor.fill()
                instructor_id = instructor.instructor_id

                time_slot_id = data['time_slot_id']

                course_sem = Course_semester(course_id, sem_id, instructor_id, time_slot_id)
                course_sem.insert()

            elif 'search' in data:
                course_name = data['course_name']
                sem_year = data['sem_year']
                sem_season = data['sem_season']
                roll_num = data['roll_num']

                course_sem_list = Course_semester.search(course_name, sem_year, sem_season, roll_num, '')
                course_sem_names = [[c.course_name, c.year, c.season, c.roll_number, c.time_slot_id, c.course_id, c.sem_id, c.instructor_id] for c in course_sem_list]
                context['course_sem_names'] = course_sem_names
            elif 'update' in data:
                #delete has more priority 
                for s in data.getlist('delete_list'):
                    s = s.split(':')
                    course_sem = Course_semester(s[0],s[1],s[2])
                    course_sem.delete()

                for u in data.getlist('update_list'):
                    uid, ucourse_id, usem_id, uinstr_id = u.split(':')
                    if ucourse_id+':'+usem_id+':'+uinstr_id in data.getlist('delete_list'):
                        continue
                    course_sem = Course_semester(ucourse_id, usem_id, uinstr_id)
                    new_course_name = data.getlist('updated_course_names')[int(uid)]
                    new_year = data.getlist('updated_years')[int(uid)]
                    new_season = data.getlist('updated_seasons')[int(uid)]
                    new_roll_num = data.getlist('updated_roll_numbers')[int(uid)]
                    new_time_slot_id = data.getlist('updated_time_slot_ids')[int(uid)]

                    new_course = Course(course_name=new_course_name)
                    new_course.fill()
                    new_course_id = new_course.course_id

                    new_sem = Semester(new_year, new_season)
                    new_sem.fill()
                    new_sem_id = new_sem.sem_id

                    new_instructor = Instructor(roll_num=new_roll_num)
                    new_instructor.fill()
                    new_instructor_id = new_instructor.instructor_id
                    course_sem.update(new_course_id, new_sem_id, new_instructor_id, new_time_slot_id)
        except:
            error = 'DB error'

    context['error'] = error 
    return render(request, 'admin/course_sem.html', context)


@user_passes_test(is_admin)
def admin_grade(request):
    error = ''
    context = {}
    if request.method == 'POST': 
        data = request.POST
        try:
            if 'add' in data:
                grade_name = data['grade_name']
                value = data['value']
                grade = Grade(grade_name, value)
                grade.insert()
            elif 'update' in data:
                #delete has more priority 
                for d in data.getlist('delete_list'):
                    grade = Grade(d)
                    grade.delete()
                for u in data.getlist('update_list'):
                    uid, uname = u.split(':')
                    if uname in data.getlist('delete_list'):
                        continue
                    grade = Grade(uname)
                    grade.update(data.getlist('updated_names')[int(uid)],data.getlist('updated_values')[int(uid)])
        except:
            error = 'DB error'

    all_grades = Grade.get_all()
    context['grade_names'] = all_grades
    context['error'] = error 
    return render(request, 'admin/grade.html', context)

@user_passes_test(is_admin)
def admin_issues(request):
    error = ''
    context = {}
    if request.method == 'POST':
        data = request.POST
        try:
            if 'search' in data:
                issues_list = Issues.search()
                context['issue_texts'] = issues_list
            elif 'update' in data:
                for u in data.getlist('update_list'):
                    uid, i_id = u.split(':')
                    issue = Issues(issue_id=int(i_id))
                    issue.update(data.getlist('replies')[int(uid)])
        except:
            error = "DB error"
    context['error'] = error
    return render(request, 'admin/issues.html', context)


@user_passes_test(is_admin)
def admin_test(request):
    return render(request, 'admin/test.html')
