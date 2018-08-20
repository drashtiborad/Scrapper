from elasticsearch import Elasticsearch

from connection import connect_sql, execute

es = Elasticsearch()
db = connect_sql()
cursor = db.cursor()

query = "select * from naukri_banglore where elasticsearch=0"
cursor.execute(query)
jd = cursor.fetchall()
columns = [col[0] for col in cursor.description]

for i in jd:
    job = dict(zip(columns, i))
    # print(job)
    data = {}
    for j in job:
        if job[j] != 'NULL':
            if isinstance(job[j], str):
                data[j] = job[j].decode("latin1")
            else:
                data[j] = job[j]
    try:
        doc = es.index(index='jobs', doc_type='job_description', id=data['id'], body=data)
        query1 = 'update naukri_banglore set elasticsearch=1 where job_id={}'.format(data['job_id'])
        execute(query1)
    except Exception as e:
        print(e)
        break
