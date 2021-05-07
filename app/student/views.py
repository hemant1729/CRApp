from django.shortcuts import render, redirect
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
            student.update(name, year, dept_id, prog_id)
        except:
            error = 'DB error'
    
    context['error'] = error
    student.fill()
    cpi, tot_credits = Student.get_cpi_credits(str(student.student_id))
    context['student_data'] = [student.name, student.year, student.prog_name, student.dept_name, cpi, tot_credits]
    return render(request, 'student/home.html', context)


@login_required(login_url='/')
def student_courses(request):
    error = ''
    context = {}
    student = Student(request.user.username)
    student.fill()
    if request.method == 'POST':
        data = request.POST
        try:
            if 'search' in data:
                course_name = data['course_name']
                year = data['year']
                season = data['season']
                instr_name = data['instr_name']
                takes = student.get_takes(course_name, year, season, instr_name)
            else:
                takes = student.get_takes('', '', '', '')
            if 'new_search' in data:
                new_course_name = data['new_course_name']
                new_year = data['new_year']
                new_season = data['new_season']
                new_instr_name = data['new_instr_name']
                new_courses_dup = Course_semester.search(new_course_name, new_year, new_season, '', new_instr_name)
                new_courses = []
                for c in new_courses_dup:
                    taken = 0
                    for t in takes:
                        if c.course_id == t.course_id and c.sem_id == t.sem_id and c.instructor_id == t.instructor_id:
                            taken = 1
                    if not taken:
                        new_courses.append(c)
                context['new_courses'] = new_courses
            if 'update' in data:
                for d in data.getlist('delete_list'):
                    d=d.split(':')
                    take = Takes(student.student_id, d[0], d[1], d[2])
                    take.delete()

                for u in data.getlist('update_list'):
                    u=u.split(':')
                    take = Takes(student.student_id, u[0], u[1], u[2])
                    take.insert()
                takes = student.get_takes('', '', '', '')
        except:
            error = 'DB error'

    else:
        takes = student.get_takes('','','','')

    context['error'] = error
    context['takes'] = takes

    return render(request, 'student/course.html', context)


@login_required(login_url='/')
def student_reviews(request):
    take_id = request.GET.get('take_id')
    try:
        if request.method=='POST':
            data = request.POST
            if 'modify' in data:
                take_id = data['take_id']
                grade_name = data['grade_name']
                num_quiz = data['num_quiz']
                num_assgn = data['num_assgn']
                exam_toughness = data['exam_toughness']
                assgn_toughness = data['assgn_toughness']
                overall_feel = data['overall_feel']
                project = data['project']
                project_details = data['project_details']
                teacher_review = data['teacher_review']
                help_availability = data['help_availability']
                working_hours = data['working_hours']
                team_size = data['team_size']
                followup_course_name = data['followup_course_name']

                if grade_name == '':
                    grade_id = None
                else:
                    grade = Grade(grade_name)
                    grade.fill()
                    grade_id = grade.grade_id
                if followup_course_name == '':
                    followup_course_id = None
                else:
                    followup_course = Course(followup_course_name)
                    followup_course.fill()
                    followup_course_id = followup_course.course_id
                review = Review(take_id=take_id)
                review.insert_data(grade_id, num_quiz, num_assgn, exam_toughness, assgn_toughness, overall_feel, project, \
                    project_details, teacher_review, help_availability, working_hours, team_size, followup_course_id)
            if 'delete' in data:
                review = Review(take_id=data['take_id'])
                review.delete()            
                return redirect('/student/courses')
        elif request.GET.get('take_id'):
            error = ''
            context = {}
            take_id = request.GET.get('take_id')
            take = Takes(take_id=take_id)
            take.fill()
            if take.roll_num != request.user.username:
                return redirect('/student/courses')
            review = Review.search(take_id) 
            if review is None:
                review = Review(take_id=take_id)
                review.insert()
                review.grade_name = None
            else:
                if review.followup_course_id is not None:
                    course = Course()
                    course.fill_id(review.followup_course_id)
                    review.followup_course_name = course.course_name
            if review.grade_name is None:
                review.grade_name = ""
            context['review'] = review
            context['error'] = error
            return render(request, 'student/modify_review.html', context)
    except:
        error = 'DB error'

    return redirect('/student/reviews/?take_id={}'.format(take_id))


def view_reviews(request):
    if request.GET.get('course_id') and request.GET.get('sem_id') and request.GET.get('instructor_id') and request.GET.get('course_name'):
        context = {}
        course_id = request.GET.get('course_id')
        sem_id = request.GET.get('sem_id')
        instructor_id = request.GET.get('instructor_id')
        reviews = Review.search_all(course_id, sem_id, instructor_id) 
        for r in reviews:
            course = Course()
            if r.followup_course_id is not None:
                course.fill_id(r.followup_course_id)
                r.followup_course_name = course.course_name
        if len(reviews) > 0:
            context['reviews'] = reviews
        context['course_name'] = request.GET.get('course_name')
        return render(request, 'student/reviews.html', context)
    return redirect('/student/courses')


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
        #try:
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
            update_student_tag_weights(student.student_id, {}, {})
        interests = Interests(student.student_id)
        tag_list = interests.get_tags()
        tag_names = [d.tag_name for d in tag_list]
        context['student_tag_names'] = tag_names
        #except:
        #    error = 'DB error'
    context['error'] = error 
    return render(request, 'student/interests.html', context)


@login_required(login_url='/')
def student_test(request):
    return render(request, 'student/test.html')

@login_required(login_url='/')
def student_timetable(request):
    student = Student(request.user.username)
    student.fill()
    timetable = Timetable(student.student_id).get_timetable()
    table = {}
    timeslots = []
    days = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    for name, day, start, end in timetable:
        timeslots.append((start, end))
    timeslots = list(set(timeslots))
    timeslots.sort()
    for day in days:
        for timeslot in timeslots:
            table[(day, timeslot)] = 'None'
    for name, day, start, end in timetable:
        table[(day, (start, end))] = name
    times = [x + '-' + y for (x, y) in timeslots]
    out = [['DAY'] + times]
    for day in days:
        cur = [day]
        for timeslot in timeslots:
            cur.append(table[(day, timeslot)])
        out.append(cur)
    context = {}
    context['table'] = out
    return render(request, 'student/timetable.html', context)

@login_required(login_url='/')
def student_recommender(request):
    student = Student(request.user.username)
    student.fill()
    similar_students = get_similar_students(student.student_id)
    out = []
    context = {}
    out = []
    for sim_stud in similar_students:
        extras = get_recommended_courses(student.student_id, sim_stud)
        cur = [get_student_name(sim_stud)]
        cur.append("<a href=\"http://127.0.0.1:8000/student/messages/?student_id={}\">Message!</a>&nbsp;".format(sim_stud))
        course_list = ""
        for c, s, i in extras:
            course_list += "<a href=\"http://127.0.0.1:8000/view_reviews/?course_id={}&sem_id={}&instructor_id={}\">{}</a>&nbsp;".format(c, s, i, get_course_name(c))
        cur.append(course_list)
        out.append(cur)
    context['recommended'] = out
    return render(request, 'student/recommender.html', context)

