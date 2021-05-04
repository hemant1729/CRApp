from django.db import models
import psycopg2

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
    
    def delete(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('DELETE FROM STUDENT WHERE prog_name={}'.format(self.prog_name))
            conn.commit()
            cur.close()
        except:
            raise Exception("connection error")

    def insert(self):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO PROGRAM (prog_name) VALUES \
            (%s)', (self.prog_name))
            conn.commit()
            cur.close()
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
            cur.execute('SELECT * FROM STUDENT WHERE roll_num=%s',(self.roll_num))
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
            cur.execute('DELETE FROM STUDENT WHERE roll_num=%s',(self.roll_num))
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
            cur.execute('SELECT * FROM STUDENT WHERE roll_num=%s',(self.roll_num))
            conn.commit()
            data = cur.fetchall()
            cur.close()
            return data
        except:
            raise Exception("connection error")
