import os
import json

hosts_var = os.getenv('HOSTS')
hosts_json = json.loads(hosts_var)

print('LOG: ' + str(len(hosts_json)) + ' hosts found')

for host in hosts_json:
    for key, value in host.items():
        print(f"{key} : {value}")
