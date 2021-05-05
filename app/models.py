from django.db import models
import psycopg2
from psycopg2.extensions import AsIs

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
            print(self.dept_name, new_name)
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
            cur.execute('SELECT tag_name FROM TAGS NATURAL JOIN COURSE_TAGS WHERE course_id=%s',(self.course_id,))
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

