import os
import json
import re

# Take the env var and make it an object (A list of dictionaries)
hosts_var = os.getenv('HOSTS')
hosts_json = json.loads(hosts_var)

# Basic log printing
print('Found: ' + str(len(hosts_json)) + ' hosts')

for host in hosts_json:
    for key, value in host.items():
        print(f"Found: {key}:{value}")

for host in hosts_json:
    print("Working on: " + host['hostname'])

    #text = "ServerName: @@hostname@@ PROXY_PASS: @@proxy_pass@@"
    with open('./src/skel.conf') as conf_file:
        conf_contents = conf_file.read()

    conf_complete = re.sub(r"@@(\w+?)@@", lambda match: host[match.group(1)], conf_contents)

    print(conf_complete)

    print("Writing /etc/nginx/conf.d/" + host['hostname'] + ".conf")

    conf_new = open("/etc/nginx/conf.d/" + host['hostname'] + ".conf", "w")
    conf_new.write(conf_complete)

