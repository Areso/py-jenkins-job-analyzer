#!/usr/bin/env python3
import requests
import json
import psycopg2
import sys

def bigf(options):
    ssl_verify = bool(options['ssl_enforce'])
    #DB connect
    try:
        cs   = """dbname   = %s 
                  host     = %s 
                  port     = %s 
                  user     = %s 
                  password = %s """ % (
                  options['db_name'],
                  options['db_host'],
                  options['db_port'],
                  options['db_user'],
                  options['db_pass'])
        conn = psycopg2.connect(cs)
    except:
        print("unable to connect to the DB")
        sys.stderr.write("unable to connect to the DB")
        sys.exit(1)
    cursor  = conn.cursor()
    #CHECKING DATABASE
    cursor.execute("SELECT * FROM job_defs WHERE job_link=%(job_name)s",
                   {"job_name": options["job_names"][0]})
    records = cursor.fetchall()
    #INSERTING IF DOESN'T EXIST
    if len(records)==0:
        cursor.execute("INSERT INTO job_defs (job_link) VALUES (%(job_name)s) RETURNING id",
                   {"job_name": options["job_names"][0]})
        rec_id = cursor.fetchall()
        conn.commit()
        job_ref_id = rec_id[0][0]
    else:
        job_ref_id = records[0][0]
    print("job_ref_id")
    print(job_ref_id)
    #STARTING GATHERING THE JOB RUNS
    address          = options['schema']+'://'+options['username']+':'+options['token']
    address          = address+'@'+options['jnk_address']+'/'+options['job_names'][0]
    for i in range(options['job_start_id'], options['job_finish_id']):
        address    = address+'/'+str(i)+'/api/json?pretty=true'
        r          = requests.get(address, verify=ssl_verify).json()
        params     = r['actions'][0]['parameters']
        params_new = {}
        for param in params:
            param_key    = param['name']
            param_value  = param['value']
            params_new[param_key] = param_value
        display_name = r['displayName']
        full_job_url = r['url']
        job_causer   = r['actions'][1]['causes']
        job_duration = r['duration']
        job_timestamp= r['timestamp']
        job_result   = r['result']
        job_executor = r['executor']
        job_timings  = r['actions'][2]
        job_git_dets = r['actions'][6]
        #INSERTING THE RESULT
        cursor.execute("""INSERT INTO job_runs (job_id, 
                                                job_run_id,
                                                params,
                                                display_name,
                                                full_job_url,
                                                job_causer,
                                                job_duration,
                                                job_timestamp,
                                                job_result,
                                                job_timings,
                                                job_git_dets)
                                                 VALUES 
                                                (%(job_id)s,
                                                 %(job_run_id)s,
                                                 %(display_name)s,
                                                 %(full_job_url)s,
                                                 %(job_causer)s,
                                                 %(job_duration)s,
                                                 %(job_timestamp)s,
                                                 %(job_result)s,
                                                 %(job_timings)s,
                                                 %(job_git_dets)s
                                                )""", {
                                                "job_id": job_ref_id,
                                                "job_run_id": i,
                                                "params": params_new,
                                                "display_name": display_name,
                                                "full_job_url": full_job_url,
                                                "job_causer": job_causer,
                                                "job_duration": job_duration,
                                                "job_result": job_result,
                                                "job_executor": job_executor,
                                                "job_timings": job_timings,
                                                "job_git_dets": job_git_dets
                                                })
        print(cursor.query)
        conn.commit()

    cursor.close()
    conn.close()


if __name__ == "__main__":
    with open('options.json') as f:
        options = json.load(f)
    bigf(options)
