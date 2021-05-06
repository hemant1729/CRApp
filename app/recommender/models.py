from django.db import models
import psycopg2
from psycopg2.extensions import AsIs

# Create your models here.
def get_connection():
    try:
        conn = psycopg2.connect(user="postgres",
                                      password="postgres",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="crapp")
        conn.autocommit = True
        return conn
    except:
        raise Exception("connection error")

def update_student_tag_weights(student_id, removed_tags, added_tags):
    try:
        conn = get_connection()
        cur = conn.cursor()
        for tag in removed_tags:
            cur.execute('UPDATE STUDENT_TAG_WEIGHTS SET count = count - %s WHERE student_id = %s AND tag_id = %s', (removed_tags[tag], student_id, tag))
        for tag in added_tags:
            cur.execute('DO \
                         $do$ \
                         BEGIN \
                         IF EXISTS (SELECT * FROM STUDENT_TAG_WEIGHTS WHERE student_id = %(student_id)s AND tag_id = %(tag_id)s) THEN \
                         UPDATE STUDENT_TAG_WEIGHTS SET count = count + %(change)s WHERE student_id = %(student_id)s AND tag_id = %(tag_id)s;  \
                         ELSE \
                         INSERT INTO STUDENT_TAG_WEIGHTS(student_id, tag_id, weight, count, in_interests) VALUES (%(student_id)s, %(tag_id)s, 0, %(change)s, 0); \
                         END IF; \
                         END \
                         $do$ \
                         ', {'student_id': student_id, 'tag_id': tag, 'change': added_tags[tag]})
        cur.execute("UPDATE STUDENT_TAG_WEIGHTS SET in_interests = (SELECT count(*) FROM interests WHERE interests.student_id = student_tag_weights.student_id AND interests.tag_id = student_tag_weights.tag_id) WHERE student_id = %s", (student_id,))
        cur.execute("DELETE FROM STUDENT_TAG_WEIGHTS WHERE count = 0 AND in_interests = 0")
        cur.execute("UPDATE STUDENT_TAG_WEIGHTS SET weight = in_interests * 0.1 + (count * 1.0) / (1.0 * (SELECT SUM(count) FROM STUDENT_TAG_WEIGHTS WHERE student_id = %s)) WHERE student_id = %s", (student_id, student_id))
        cur.execute("UPDATE STUDENT_TAG_WEIGHTS SET weight = (weight * 1.0) / (SELECT sqrt(SUM(weight*weight)) FROM STUDENT_TAG_WEIGHTS WHERE student_id = %s) WHERE student_id = %s", (student_id,student_id))
        cur.close()
    except:
        raise Exception("connection error")

def get_similar_students(student_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT student_id, SUM(dot) as distance FROM (SELECT s.student_id, r.weight * s.weight as dot FROM STUDENT_TAG_WEIGHTS r, STUDENT_TAG_WEIGHTS s WHERE r.student_id = %(student_id)s AND s.student_id <> %(student_id)s AND r.tag_id = s.tag_id) as t GROUP BY student_id ORDER BY distance DESC LIMIT 5", {'student_id': student_id})
        data = cur.fetchall()
        out = []
        for d in data:
            out.append(Student(d[0]))
        return out
        cur.close()
    except:
        raise Exception("connection error")

def get_recommended_courses(student_id):
    try:
        out = []
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT course_id from takes where student_id = %s", (student_id,))
        done = [d[0] for d in cur.fetchall()]
        cur.close()
        students = get_similar_students(student_id)
        for student in students:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT course_id from takes where student_id = %s", (student,))
            extras = [d[0] for d in cur.fetchall()]
            out += list(set(extras) - set(done))
            cur.close()
        return out
    except:
        raise Exception("connection error")