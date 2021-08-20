#!/usr/bin/env python3
import requests

schema   = 'https://'
ssl_sign_enforce = False
jnk_address = ''

username = ''
token    = ''

job_name = ''
address  = schema+username+':'+token+'@'+jnk_address+'/'+job_name
job_id   = 0

address  = address+'/'+str(job_id)+'/api/python?pretty=true'
r = requests.get(address, verify=ssl_sign_enforce)
print(r)
