import time
import psycopg2
import statistics
from .models import get_connection




def course_trigger():
    stat_names = ['num_quiz', 'num_assgn', 'exam_toughness', 'assgn_toughness', 'overall_feel', 'project', 'help_availability', 'working_hours', 'team_size']
    stat_type = ['mode', 'mode', 'mean', 'mean', 'mean', 'mode', 'mean', 'mean', 'mode']
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

    con
    for k in agg_stat_dict:
        query = "UPDATE COURSE_SEMESTER SET (num_quiz, num_assgn, exam_toughness, overall_feel, project, help_availiability, working_hours, team_size) = \
            ({}, {}, {}, {}, {}, {}, {}, {}, {}) WHERE course_id={} AND sem_id={} AND instructor_id={}".format(*agg_stat_dict[k], k[1], k[0], k[2])
        

    cur.close()
    
    

if __name__=='__main__':
    try:
        course_trigger()
    except:
        print('Failed to update trigger')
    time.sleep(10)
    print('Course table values updated')