from django.db import models
import psycopg2
from psycopg2.extensions import AsIs
from app.recommender.models import *

# Create your models here.
def get_connection():
    try:
        conn = psycopg2.connect(user="postgres",
                                      password="!Bwsl123",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="crapp")
        return conn
    except:
        raise Exception("connection error")


class Program:
    def __init__(self, prog_name=None):
        self.prog_name = prog_name
    
    def fill(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM PROGRAM WHERE prog_name=%s',(self.prog_name,))
            conn.commit()
            data = cur.fetchone()
            self.prog_id = data[0]
            cur.close()
        except:
            raise Exception("connection error")

    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM PROGRAM WHERE prog_name=%s',(self.prog_name,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def update(self, new_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE PROGRAM SET prog_name=%s WHERE prog_name=%s', (new_name, self.prog_name))
            conn.commit()
            cur.close()
            self.prog_name = new_name
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO PROGRAM (prog_name) VALUES (%s)', (self.prog_name,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    @staticmethod
    def search(prog_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM PROGRAM WHERE prog_name ILIKE %(prog_name)s||'%%'", {'prog_name': prog_name})
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                prog_name = d[1]
                output.append(Program(prog_name=prog_name))
            cur.close()
            return output
        except:
            raise Exception("connection error")


class Department:
    def __init__(self, dept_name=None):
        self.dept_name = dept_name
    
    def fill(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM DEPARTMENT WHERE dept_name=%s',(self.dept_name,))
            conn.commit()
            data = cur.fetchone()
            self.dept_id = data[0]
            cur.close()
        except:
            raise Exception("connection error")

    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM DEPARTMENT WHERE dept_name=%s',(self.dept_name,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def update(self, new_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE DEPARTMENT SET dept_name=%s WHERE dept_name=%s', (new_name, self.dept_name))
            conn.commit()
            cur.close()
            self.dept_name = new_name
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO DEPARTMENT (dept_name) VALUES (%s)', (self.dept_name,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    @staticmethod
    def search(dept_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM DEPARTMENT WHERE dept_name ILIKE %(dept_name)s||'%%'", {'dept_name': dept_name})
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                dept_name = d[1]
                output.append(Department(dept_name=dept_name))
            cur.close()
            return output
        except:
            raise Exception("connection error")



class Course:
    def __init__(self, course_name=None, dept_id=None, credits = None):
        self.course_name = course_name
        self.dept_id = dept_id
        self.credits = credits


    def fill(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT course_id FROM COURSE WHERE course_name=%s',(self.course_name,))
            conn.commit()
            data = cur.fetchone()
            self.course_id = data[0]
            cur.close()
        except:
            raise Exception("connection error")

    def fill_id(self, course_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM COURSE WHERE course_id=%s',(course_id,))
            conn.commit()
            data = cur.fetchone()
            self.course_id = data[0]
            self.course_name = data[1]
            self.dept_id = data[2]
            self.credits = data[3]
            cur.close()
        except:
            raise Exception("connection error")

    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM COURSE WHERE course_name=%s',(self.course_name,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def update(self, new_course_name, new_dept_id, new_credits):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE COURSE SET (course_name, dept_id, credits) = (%s, %s, %s) WHERE course_name=%s', \
            (new_course_name, new_dept_id, new_credits, self.course_name))
            conn.commit()
            cur.close()
            self.course_name = new_course_name
            self.dept_id = new_dept_id
            self.credits = new_credits
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO COURSE (course_name, dept_id, credits) VALUES (%s, %s, %s)', (self.course_name, self.dept_id, self.credits))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    @staticmethod
    def search(course_name, dept_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            if dept_name != '':
                cur.execute("SELECT * FROM COURSE LEFT JOIN DEPARTMENT USING (dept_id) WHERE course_name ILIKE %(course_name)s||'%%' AND dept_name ILIKE \
                    %(dept_name)s||'%%'", {'course_name': course_name,'dept_name': dept_name})
            else:
                cur.execute("SELECT * FROM COURSE LEFT JOIN DEPARTMENT USING (dept_id) WHERE course_name ILIKE %(course_name)s||'%%'", \
                    {'course_name': course_name,'dept_name': dept_name})
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                course_name = d[2]
                dept_id = d[0]
                credits = d[4]
                course = Course(course_name=course_name, dept_id=dept_id, credits=credits)
                course.dept_name = d[5]
                course.course_id = d[1]
                output.append(course)
            cur.close()
            return output
        except:
            raise Exception("connection error")


class Instructor:
    def __init__(self, roll_num=None, instr_name=None, dept_id=None):
        self.roll_num = roll_num
        self.instr_name = instr_name
        self.dept_id = dept_id


    def fill(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT instructor_id FROM INSTRUCTOR WHERE roll_num=%s',(self.roll_num,))
            conn.commit()
            data=cur.fetchone()
            self.instructor_id = data[0]
            cur.close()
        except:
            raise Exception("connection error")


    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM INSTRUCTOR WHERE roll_num=%s',(self.roll_num,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def update(self, new_roll_num, new_instr_name, new_dept_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE INSTRUCTOR SET (roll_num, instr_name, dept_id) = (%s, %s, %s) WHERE roll_num=%s', \
            (new_roll_num, new_instr_name, new_dept_id, self.roll_num))
            conn.commit()
            cur.close()
            self.roll_num = new_roll_num
            self.instr_name = new_instr_name
            self.dept_id = new_dept_id
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO INSTRUCTOR (roll_num, instr_name, dept_id) VALUES (%s, %s, %s)', (self.roll_num, self.instr_name, self.dept_id))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    @staticmethod
    def search(roll_num, instr_name, dept_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            if dept_name != '':
                cur.execute("SELECT * FROM INSTRUCTOR LEFT JOIN DEPARTMENT USING (dept_id) WHERE roll_num ILIKE %(roll_num)s||'%%'\
                    AND instr_name ILIKE %(instr_name)s||'%%' AND dept_name ILIKE %(dept_name)s||'%%'", \
                        {'roll_num': roll_num, 'instr_name': instr_name, 'dept_name': dept_name})
            else:
                cur.execute("SELECT * FROM INSTRUCTOR LEFT JOIN DEPARTMENT USING (dept_id) WHERE roll_num ILIKE %(roll_num)s||'%%' AND \
                    instr_name ILIKE %(instr_name)s||'%%'", {'roll_num': roll_num, 'instr_name': instr_name})
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                roll_num = d[2]
                instr_name = d[3]
                dept_id = d[0]
                instr = Instructor(roll_num=roll_num, instr_name=instr_name, dept_id=dept_id)
                instr.dept_name = d[4]
                output.append(instr)
            cur.close()
            return output
        except:
            raise Exception("connection error")


class Semester:
    def __init__(self, year=None, season=None):
        self.year = year
        self.season = season

    def fill(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT sem_id FROM SEMESTER WHERE year=%s AND season=%s',(self.year, self.season))
            conn.commit()
            data = cur.fetchone()
            self.sem_id = data[0]
            cur.close()
        except:
            raise Exception("connection error")


    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM SEMESTER WHERE year=%s AND season=%s',(self.year, self.season))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def update(self, new_year, new_season):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE SEMESTER SET (year, season) = (%s, %s) WHERE year=%s AND season=%s', \
            (new_year, new_season, self.year, self.season))
            conn.commit()
            cur.close()
            self.year = new_year
            self.season = new_season
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO SEMESTER (year, season) VALUES (%s, %s)', (self.year, self.season))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    @staticmethod
    def search(year, season):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM SEMESTER WHERE CAST(year as TEXT) ILIKE %(year)s||'%%' \
                AND CAST(season as TEXT) ILIKE %(season)s||'%%'", {'year': year, 'season': season})
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                year = d[1]
                season = d[2]
                sem = Semester(year=year, season=season)
                output.append(sem)
            cur.close()
            return output
        except:
            raise Exception("connection error")


class Timeslot:
    def __init__(self, time_slot_id=None, day=None, start_time=None, end_time=None):
        self.time_slot_id = time_slot_id
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM TIMESLOT WHERE time_slot_id=%s AND day=%s AND start_time=%s AND end_time=%s',\
                (self.time_slot_id, self.day, self.start_time, self.end_time))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def update(self, new_time_slot_id, new_day, new_start_time, new_end_time):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE TIMESLOT SET (time_slot_id, day, start_time, end_time) = (%s, %s, %s, %s) WHERE time_slot_id=%s AND \
                day=%s AND start_time=%s AND end_time=%s', \
            (new_time_slot_id, new_day, new_start_time, new_end_time, self.time_slot_id, self.day, self.start_time, self.end_time))
            conn.commit()
            cur.close()
            self.time_slot_id = new_time_slot_id
            self.day = new_day
            self.start_time = new_start_time
            self.end_time = new_end_time
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO TIMESLOT (time_slot_id, day, start_time, end_time) VALUES (%s, %s, %s, %s)', \
                (self.time_slot_id, self.day, self.start_time, self.end_time))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    @staticmethod
    def search(time_slot_id, day, start_time, end_time):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM TIMESLOT WHERE time_slot_id ILIKE %(time_slot_id)s||'%%' AND day ILIKE %(day)s||'%%'\
                AND CAST(start_time AS TEXT) ILIKE %(start_time)s||'%%' AND CAST(end_time AS TEXT) ILIKE %(end_time)s||'%%'", \
                    {'time_slot_id': time_slot_id,'day': day, 'start_time': start_time, 'end_time': end_time})
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                time_slot_id = d[0]
                day = d[1]
                start_time = d[2].strftime('%H:%M')
                end_time = d[3].strftime('%H:%M')
                timeslot = Timeslot(time_slot_id=time_slot_id, day=day, start_time=start_time, end_time=end_time)
                output.append(timeslot)
            cur.close()
            return output
        except:
            raise Exception("connection error")


class Student:
    def __init__(self, roll_num=None, name=None, year=None, program_id=None, cpi=None, tot_credits=None, dept_id=None):
        self.roll_num = roll_num
        self.name = name
        self.year = year
        self.program_id = program_id
        self.cpi = cpi
        self.tot_credits = tot_credits
        self.dept_id = dept_id

    def fill(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM (STUDENT LEFT JOIN DEPARTMENT USING (dept_id)) LEFT JOIN PROGRAM USING (program_id) WHERE roll_num=%s', (self.roll_num,))
            conn.commit()
            data = cur.fetchone()
            self.name = data[4]
            self.year = data[5]
            self.program_id = data[0]
            self.cpi = data[6]
            self.tot_credits = data[7]
            self.dept_name = data[8]
            self.prog_name = data[9]
            self.dept_id = data[1]
            self.student_id = data[2]

            cur.close()
        except:
            raise Exception("connection error")

    def update(self,name,year,dept_id,prog_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE STUDENT SET (name, year, dept_id, program_id)=(%s, %s, %s,%s) WHERE roll_num=%s', (name, year, dept_id, prog_id, self.roll_num))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM STUDENT WHERE roll_num=%s', (self.roll_num,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO STUDENT (roll_num, name, year, program_id, cpi, tot_credits, dept_id) VALUES \
            (%s, %s, %s, %s, %s, %s, %s)', (self.roll_num, self.name, self.year, self.program_id, self.cpi, self.tot_credits, self.dept_id))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def get_takes(self, course_name, sem_year, sem_season, instr_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM TAKES NATURAL JOIN ((COURSE_SEMESTER NATURAL JOIN COURSE NATURAL JOIN SEMESTER) INNER JOIN INSTRUCTOR USING (instructor_id))\
                 WHERE student_id=%(student_id)s AND course_name ILIKE %(course_name)s||'%%' AND CAST(year AS TEXT) ILIKE %(year)s||'%%' \
                     AND CAST(season AS TEXT) ILIKE %(season)s||'%%' AND instr_name ILIKE '%%'||%(instr_name)s||'%%'", \
                         {'student_id':self.student_id, 'course_name': course_name, 'year': sem_year, 'season': sem_season, 'instr_name': instr_name})
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                course_semester = Course_semester(course_id=d[1], sem_id=d[0], instructor_id=d[2])
                course_semester.course_name = d[16]
                course_semester.year = d[20]
                course_semester.season = d[21]
                course_semester.instr_roll_num = d[22]
                course_semester.instr_name = d[23]
                course_semester.take_id = d[3]
                output.append(course_semester)
            cur.close()
            return output
        except:
            raise Exception("connection error")

    @staticmethod
    def search():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM STUDENT WHERE roll_num=%s', (self.roll_num,))
            conn.commit()
            data = cur.fetchall()
            cur.close()
            return data
        except:
            raise Exception("connection error")


    @staticmethod
    def get_cpi_credits(student_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT value, credits FROM (((REVIEW NATURAL JOIN TAKES) INNER JOIN COURSE_SEMESTER USING (course_id, sem_id, instructor_id) \
                INNER JOIN GRADE USING (grade_id)) INNER JOIN COURSE USING (course_id)) \
                    WHERE student_id=%s', (student_id,))
            conn.commit()
            data = cur.fetchall()
            tot_points = 0
            tot_credits = 0
            for d in data:
                tot_credits += d[1]
                tot_points += d[0]*d[1]
            if tot_credits == 0:
                return 0, 0
            else:
                return round(tot_points/tot_credits, 2), tot_credits
            cur.close()
        except:
            raise Exception("connection error")


class Tag:
    def __init__(self, tag_name=None):
        self.tag_name = tag_name
    
    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM TAGS WHERE tag_name=%s',(self.tag_name,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def update(self, new_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE TAGS SET tag_name=%s WHERE tag_name=%s', (new_name, self.tag_name))
            conn.commit()
            cur.close()
            self.tag_name = new_name
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO TAGS (tag_name) VALUES (%s)', (self.tag_name,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    @staticmethod
    def search(tag_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM TAGS WHERE tag_name ILIKE %(tag_name)s||'%%'", {'tag_name': tag_name})
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                tag_name = d[1]
                output.append(Tag(tag_name=tag_name))
            cur.close()
            return output
        except:
            raise Exception("connection error")


class Course_tags:
    def __init__(self, course_id=None):
        self.course_id = course_id

    def get_tags(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT tag_name, tag_id FROM TAGS NATURAL JOIN COURSE_TAGS WHERE course_id=%s',(self.course_id,))
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                tag_name = d[0]
                tag_id = d[1]
                tag = Tag(tag_name=tag_name)
                tag.tag_id = tag_id
                output.append(tag)
            cur.close()
            return output
        except:
            raise Exception("connection error")

    def get_name(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT course_name FROM COURSE WHERE course_id=%s',(self.course_id,))
            conn.commit()
            data = cur.fetchall()
            cur.close()
            return data[0][0]
        except:
            raise Exception("connection error")
    def remove_tag(self, tag_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM COURSE_TAGS WHERE course_id=%s AND tag_id = (SELECT tag_id FROM TAGS WHERE tag_name=%s)',(self.course_id,tag_name))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def add_tag(self, tag_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO COURSE_TAGS(course_id, tag_id) VALUES (%s, (SELECT tag_id FROM TAGS WHERE tag_name=%s))', (self.course_id,tag_name))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")


class Course_semester:
    def __init__(self, course_id=None, sem_id=None, instructor_id=None):
        self.course_id = course_id
        self.sem_id = sem_id
        self.instructor_id = instructor_id

    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM COURSE_SEMESTER WHERE course_id=%s AND sem_id=%s AND instructor_id=%s',\
                (self.course_id, self.sem_id, self.instructor_id))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def update(self, new_course_id, new_sem_id, new_instructor_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE COURSE_SEMESTER SET (course_id, sem_id, instructor_id) = (%s, %s, %s) WHERE course_id=%s AND \
                sem_id=%s AND instructor_id=%s', \
            (new_course_id, new_sem_id, new_instructor_id, self.course_id, self.sem_id, self.instructor_id))
            conn.commit()
            cur.close()
            self.course_id = new_course_id
            self.sem_id = new_sem_id
            self.instructor_id = new_instructor_id
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO COURSE_SEMESTER (course_id, sem_id, instructor_id) VALUES (%s, %s, %s)', \
                (self.course_id, self.sem_id, self.instructor_id))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def get_reviews(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT * REVIEW WHERE sem_id=%s AND course_id=%s AND instructor_id=%s', (self.sem_id, self.course_id, self.instructor_id))
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:

                output.append()
            cur.close()
        except:
            raise Exception("connection error")


    @staticmethod
    def search(course_name, sem_year, sem_season, instr_roll_num, instr_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM (COURSE_SEMESTER NATURAL JOIN COURSE NATURAL JOIN SEMESTER) INNER JOIN INSTRUCTOR USING (instructor_id)\
                 WHERE course_name ILIKE %(course_name)s||'%%' AND CAST(year AS TEXT) ILIKE %(year)s||'%%' \
                     AND CAST(season AS TEXT) ILIKE %(season)s||'%%' AND roll_num ILIKE %(roll_num)s||'%%' AND instr_name ILIKE '%%'||%(instr_name)s||'%%'", \
                         {'course_name': course_name, 'year': sem_year, 'season': sem_season, 'roll_num': instr_roll_num, 'instr_name': instr_name})
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                course_id = d[2]
                sem_id = d[1]
                instructor_id = d[0]
                course_semester = Course_semester(course_id=course_id, sem_id=sem_id, instructor_id=instructor_id)
                course_semester.course_name = d[14]
                course_semester.year = d[18]
                course_semester.season = d[19]
                course_semester.roll_number = d[20]
                course_semester.instr_name = d[21]

                course_semester.num_quiz = d[5]
                course_semester.num_assgn = d[6]
                course_semester.exam_toughness = d[7]
                course_semester.assgn_toughness = d[8]
                course_semester.overall_feel = d[9]
                course_semester.project = d[10]
                course_semester.help_availability = d[11]
                course_semester.working_hours = d[12]
                course_semester.team_size = d[13]
                output.append(course_semester)
            cur.close()
            return output
        except:
            raise Exception("connection error")


class Takes:
    def __init__(self, student_id=None, course_id=None, sem_id=None,instructor_id=None, take_id=None):
        self.student_id = student_id
        self.sem_id = sem_id
        self.course_id = course_id
        self.instructor_id = instructor_id
        self.take_id = take_id

    def fill(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT * FROM TAKES NATURAL JOIN STUDENT WHERE take_id=%s', (self.take_id,))
            conn.commit()
            data = cur.fetchone()
            if data is not None:
                self.student_id = data[0]
                self.sem_id = data[2]
                self.course_id = data[3]
                self.instructor_id = data[4]
                self.roll_num = data[5]
            cur.close()
        except:
            raise Exception("connection error")

    def delete(self):
        try:
            course_tags = Course_tags(course_id=self.course_id)
            tags_list = course_tags.get_tags()
            tag_dict = {}
            for t in tags_list:
                tag_dict[str(t.tag_id)]='1'
            update_student_tag_weights(self.student_id, tag_dict, {})

            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM TAKES WHERE student_id=%s AND sem_id=%s AND course_id=%s AND instructor_id=%s',\
                (self.student_id, self.sem_id, self.course_id, self.instructor_id))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")


    def insert(self):
        try:
            course_tags = Course_tags(course_id=self.course_id)
            tags_list = course_tags.get_tags()
            tag_dict = {}
            for t in tags_list:
                tag_dict[str(t.tag_id)]='1'
            update_student_tag_weights(self.student_id, {}, tag_dict)

            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO TAKES (student_id, sem_id, course_id, instructor_id) VALUES (%s, %s, %s, %s)', \
                (self.student_id, self.sem_id, self.course_id, self.instructor_id))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")


    @staticmethod
    def search(course_name, sem_year, sem_season, instr_roll_num):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM (COURSE_SEMESTER NATURAL JOIN COURSE NATURAL JOIN SEMESTER) INNER JOIN INSTRUCTOR USING (instructor_id)\
                 WHERE course_name ILIKE %(course_name)s||'%%' AND CAST(year AS TEXT) ILIKE %(year)s||'%%' \
                     AND CAST(season AS TEXT) ILIKE %(season)s||'%%' AND roll_num ILIKE %(roll_num)s||'%%'", \
                         {'course_name': course_name, 'year': sem_year, 'season': sem_season, 'roll_num': instr_roll_num})
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                course_id = d[2]
                sem_id = d[1]
                instructor_id = d[0]
                course_semester = Course_semester(course_id=course_id, sem_id=sem_id, instructor_id=instructor_id)
                course_semester.course_name = d[14]
                course_semester.year = d[18]
                course_semester.season = d[19]
                course_semester.roll_number = d[20]
                output.append(course_semester)
            cur.close()
            return output
        except:
            raise Exception("connection error")


class Interests:
    def __init__(self, student_id=None):
        self.student_id = student_id

    def get_tags(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT tag_name FROM TAGS NATURAL JOIN INTERESTS WHERE student_id=%s',(self.student_id,))
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                tag_name = d[0]
                output.append(Tag(tag_name=tag_name))
            cur.close()
            return output
        except:
            raise Exception("connection error")

    def remove_tag(self, tag_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM INTERESTS WHERE student_id=%s AND tag_id = (SELECT tag_id FROM TAGS WHERE tag_name=%s)',(self.student_id,tag_name))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def add_tag(self, tag_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO INTERESTS(student_id, tag_id) VALUES (%s, (SELECT tag_id FROM TAGS WHERE tag_name=%s))', (self.student_id,tag_name))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")


class Grade:
    def __init__(self, grade_name=None, value=None):
        self.grade_name = grade_name
        self.value = value

    def fill(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('SELECT grade_id FROM GRADE WHERE grade_name=%s',(self.grade_name,))
            conn.commit()
            data = cur.fetchone()
            self.grade_id = data[0]
            cur.close()
        except:
            raise Exception("connection error")

    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM GRADE WHERE grade_name=%s',(self.grade_name,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def update(self, new_grade_name, new_grade_value):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE GRADE SET (grade_name, value) = (%s, %s) WHERE grade_name=%s', \
            (new_grade_name, new_grade_value, self.grade_name))
            conn.commit()
            cur.close()
            self.grade_name = new_grade_name
            self.grade_value = new_grade_value
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO GRADE (grade_name, value) VALUES (%s, %s)', (self.grade_name, self.value))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    @staticmethod
    def get_all():
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM GRADE")
            conn.commit()
            data = cur.fetchall()
            cur.close()
            return data
        except:
            raise Exception("connection error")


class Review:
    def __init__(self, take_id=None):
        self.take_id = take_id

    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM REVIEW WHERE take_id=%s' ,(self.take_id,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO REVIEW (take_id, project_desc, teacher_review) VALUES (%s, %s, %s)', (self.take_id, "", ""))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def insert_data(self, grade_id, num_quiz, num_assgn, exam_toughness, assgn_toughness, overall_feel, project, project_desc, teacher_review, help_availability, working_hours, team_size, followup_course_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE REVIEW SET (grade_id, num_quiz, num_assgn, exam_toughness, assgn_toughness, overall_feel, project, \
                project_desc, teacher_review, help_availability, working_hours, team_size, followup_course_id) = (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) \
                    WHERE take_id=%s',  (grade_id, num_quiz, num_assgn, exam_toughness, assgn_toughness, overall_feel, project, project_desc, \
                        teacher_review, help_availability, working_hours, team_size, followup_course_id, self.take_id))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    @staticmethod
    def search(take_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM (((REVIEW NATURAL JOIN TAKES) LEFT JOIN GRADE USING (grade_id))) WHERE take_id=%s", (take_id,))
            conn.commit()
            data = cur.fetchall()
            output = None
            if len(data)>0:
                data=data[0]
                output = Review(take_id=take_id)
                output.grade_id = data[0]
                output.num_quiz = data[2]
                output.num_assgn = data[3]
                output.exam_toughness = data[4]
                output.assgn_toughness = data[5]
                output.overall_feel = data[6]
                output.project = data[7]
                output.project_description = data[8]
                output.teacher_review = data[9]
                output.help_availability = data[10]
                output.working_hours = data[11]
                output.team_size = data[12]
                output.followup_course_id = data[13]
                output.grade_name = data[18]
            cur.close()
            return output
        except:
            raise Exception("connection error")

    @staticmethod
    def search_all(course_id, sem_id, instructor_id):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM (((((REVIEW INNER JOIN TAKES USING (take_id)) INNER JOIN COURSE USING (course_id)) \
                INNER JOIN INSTRUCTOR USING (instructor_id)) INNER JOIN SEMESTER USING(sem_id)) INNER JOIN STUDENT USING (student_id)) WHERE \
                    course_id=%s AND sem_id=%s AND instructor_id=%s", (course_id, sem_id, instructor_id))
            conn.commit()
            data = cur.fetchall()
            output = []
            for d in data:
                review = Review()
                review.num_quiz = d[6]
                review.num_assgn = d[7]
                review.exam_toughness = d[8]
                review.assng_toughness = d[9]
                review.overall_feel = d[10]
                review.project = d[11]
                review.project_desc = d[12]
                review.teacher_review = d[13]
                review.help_availability = d[14]
                review.working_hours = d[15]
                review.team_size = d[16]
                review.followup_course_id = d[17]
                review.course_name = d[18]

                review.instr_name = d[23]
                review.year = d[25]
                review.season = d[26]
                review.student_roll_num = d[27]
                review.student_name = d[28]
                output.append(review)

            return output
            cur.close()
        except:
            raise Exception("connection error")

class Timetable:
    def __init__(self, student_id=None):
        self.student_id = student_id
    def get_timetable(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('select course_name, day, start_time, end_time from student_sem natural join takes natural join course_semester natural join timeslot natural join course where student_sem.student_id = %s', (self.student_id,))
            conn.commit()
            data = cur.fetchall()
            out = [(d[0], d[1], d[2].strftime('%H:%M'), d[3].strftime('%H:%M')) for d in data]
            cur.close()
            return out
        except:
            raise Exception("connection error")
