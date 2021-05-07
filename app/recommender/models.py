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
        return conn
    except:
        raise Exception("connection error")

def update_student_tag_weights(student_id, removed_tags, added_tags):
    alpha = 0.5
    print(removed_tags)
    print(added_tags)
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
        cur.execute("INSERT INTO STUDENT_TAG_WEIGHTS(student_id, tag_id, weight, count, in_interests) \
            SELECT student_id, tag_id, 0.0, 0, 1 \
                FROM INTERESTS s \
                    WHERE NOT EXISTS (SELECT 1 FROM STUDENT_TAG_WEIGHTS t WHERE t.student_id = s.student_id AND t.tag_id = s.tag_id)")
        cur.execute("UPDATE STUDENT_TAG_WEIGHTS SET in_interests = (SELECT count(*) FROM interests WHERE interests.student_id = student_tag_weights.student_id AND interests.tag_id = student_tag_weights.tag_id) WHERE student_id = %s", (student_id,))
        cur.execute("DELETE FROM STUDENT_TAG_WEIGHTS WHERE count = 0 AND in_interests = 0")
        cur.execute("UPDATE STUDENT_TAG_WEIGHTS SET weight = in_interests * %s + (count * 1.0) / (1.0 * (SELECT GREATEST(CAST(1 AS BIGINT), SUM(count)) FROM STUDENT_TAG_WEIGHTS WHERE student_id = %s)) WHERE student_id = %s", (alpha, student_id, student_id))
        cur.execute("UPDATE STUDENT_TAG_WEIGHTS SET weight = (weight * 1.0) / (SELECT sqrt(SUM(weight*weight)) FROM STUDENT_TAG_WEIGHTS WHERE student_id = %s) WHERE student_id = %s", (student_id,student_id))
        conn.commit()
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
            out.append(d[0])
        return out
        cur.close()
    except:
        raise Exception("connection error")

def get_recommended_courses(student_id1, student_id2):
    try:
        out = []
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT course_id from takes where student_id = %s", (student_id1,))
        done = {d[0] for d in cur.fetchall()}
        cur.close()
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT course_id, sem_id, instructor_id from takes where student_id = %s", (student_id2,))
        extras = []
        data = cur.fetchall()
        for d in data:
            if d[0] not in done:
                extras.append((d[0], d[1], d[2]))
        cur.close()
        return extras
    except:
        raise Exception("connection error")
def get_student_name(student_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name from student where student_id=%s", (student_id,))
        data = cur.fetchall()
        return data[0][0]
    except:
        raise Exception("connection")

def get_course_name(course_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT course_name from course where course_id=%s", (course_id,))
        data = cur.fetchall()
        return data[0][0]
    except:
        raise Exception("connection")

def get_similar_courses(student_id):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("with temp(course_id, tag_id, w) as (select course_id, tag_id, 1.0 / h from (select course_id, SQRT(COUNT(*)) as h from course_tags group by course_id) as x natural join course_tags) \
                     SELECT course_id, SUM(weight * w) as t FROM student_tag_weights natural join temp WHERE student_id = %s GROUP BY course_id ORDER BY t DESC LIMIT 5\
                    ", (student_id,))
        data = cur.fetchall()
        out = [d[0] for d in data]
        cur.close()
        return out
    except:
         raise Exception("connection")