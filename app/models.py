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


class Course:
    def __init__(self, course_name=None, dept_id=None, credits = None):
        self.course_name = course_name
        self.dept_name = dept_name
        self.credits = credits

    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM COURSE WHERE course_name=%s',(self.course_name,))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def update(self, new_course_name, new_dept_name, new_credits):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('UPDATE COURSE SET (course_name, dept_name, credits) = (COALESCE(%s,%s), COALESCE(%s,%s), COALESCE(%s,%s)) WHERE course_name=%s', \
            (new_course_name, AsIs('course_name'), new_dept_name, AsIs('dept_name'), new_credits, AsIs('credits'), self.course_name))
            conn.commit()
            cur.close()
            if new_course_name:
                self.course_name = new_course_name
            if new_dept_name:
                self.dept_name = new_dept_name
            if new_credits:
                self.credits = new_credits
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO COURSE (course_name, dept_name, credits) VALUES (%s, %s, %s)', (self.course_name, self.dept_name, self.credits))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    @staticmethod
    def search(course_name, dept_name):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM DEPARTMENT WHERE course_name ILIKE %(course_name)s||'%%' AND dept_name ILIKE %(dept_name)s||'%%'", \
                {'course_name': course_name,'dept_name': dept_name})
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




class Department:
    def __init__(self, dept_name=None):
        self.dept_name = dept_name
    
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


class Program:
    def __init__(self, prog_name=None):
        self.prog_name = prog_name
    
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
            cur.execute('SELECT * FROM STUDENT WHERE roll_num=%s', (self.roll_num,))
            conn.commit()
            data = cur.fetchone()
            self.name, self.year, self.program_id, self.cpi, self.tot_credits, self.dept_id = data[2:]
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
    def search(self):
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
