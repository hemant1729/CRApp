import time
import psycopg2
import statistics


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


def course_trigger():
    stat_names = ['num_quiz', 'num_assgn', 'exam_toughness', 'assgn_toughness', 'overall_feel', 'project', 'help_availability', 'working_hours', 'team_size']
    stat_type = ['mode', 'mode', 'mean', 'mean', 'mean', 'mode', 'mean', 'mode', 'mode']
    stat_count = len(stat_names)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM REVIEW INNER JOIN TAKES USING (take_id)')
    conn.commit()
    data = cur.fetchall()
    stat_dict = {}
    for d in data:
        sem_id = d[15]
        course_id = d[16]
        instructor_id = d[17]
        stat_data = d[2:8]+d[10:13]
        if (sem_id, course_id, instructor_id) not in stat_dict:
            stat_dict[(sem_id, course_id, instructor_id)] = [stat_data]
        else:
            stat_dict[(sem_id, course_id, instructor_id)].append(stat_data)
    agg_stat_dict = {k:[] for k in stat_dict}
    for i in range(stat_count):
        for k in stat_dict:
            k_stats = stat_dict[k]
            stat_list = []
            for s in k_stats:
                if s[i] != '':
                    stat_list.append(int(s[i])) 
            if len(stat_list)==0:
                stat = None
            elif stat_type[i] == 'mode':
                stat = statistics.mode(stat_list)
            elif stat_type[i] == 'mean':
                stat = statistics.mean(stat_list)
            agg_stat_dict[k].append(stat)

    conn = get_connection()
    cur = conn.cursor()
    for k in agg_stat_dict:
        query = "UPDATE COURSE_SEMESTER SET (num_quiz, num_assgn, exam_toughness, assgn_toughness, overall_feel, project, help_availability, working_hours, team_size) = \
            (%s, %s, %s, %s, %s, %s, %s, %s, %s) WHERE course_id=%s AND sem_id=%s AND instructor_id=%s"
        cur.execute(query, (*agg_stat_dict[k], k[1], k[0], k[2]))
    conn.commit()
    cur.close()
    
    

if __name__=='__main__':
    try:
        course_trigger()
    except:
        print('Failed to update trigger')
    time.sleep(10)

    print('Course table values updated')