#!/usr/bin/env python3
import requests

jenkins_address = ''
job_name = ''
address = jenkins_address+'/'+job_name
job_id  = 0
address = address+'/'+str(job_id)+'/api/python?pretty=true'
r = requests.get(address)
print(r)
