#!/usr/bin/env python3
import requests
import json


 def bigf(options):
    address          = options['schema']+'://'+options['username']+':'+options['token']
    address          = address+'@'+options['jnk_address']+'/'+options['job_names'][0]
    address    = address+'/'+str(options['job_id'])+'/api/json?pretty=true'
    ssl_verify = bool(options['ssl_enforce']

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


if __name__ == "__main__":
    with open('options.json') as f:
        options = json.load(f)
    bigf(options)
