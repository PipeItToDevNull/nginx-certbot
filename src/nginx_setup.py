import os
import json
import re

# Take the env var and make it an object (A list of dictionaries)
hosts_var = os.getenv('HOSTS')
hosts_json = json.loads(hosts_var)

email = os.getenv('EMAIL')
prod = os.getenv('PRODUCTION')

# copy in any manual conf files the user made
os.system("cp -rf /etc/nginx/conf.avail/*.conf /etc/nginx/conf.d/ &> /dev/null")
print("LOG: Configurations present: " + str(os.listdir("/etc/nginx/conf.d")))

# Basic log printing
print('LOG: Found: ' + str(len(hosts_json)) + ' hosts')

for host in hosts_json:
    for key, value in host.items():
        print(f"LOG: Found: {key}:{value}")

for host in hosts_json:
    print("LOG: Working on: " + host['hostname'])

    if "hostname" in host:
        print("LOG: " + host['hostname'] + " is valid")

        if "proxy_pass" in host:
            print("LOG: " + host['hostname'] + " has proxy_pass " + host['proxy_pass'] + " creating conf file")

            # configuration file creation
            with open('/root/skel.conf') as conf_file:
                conf_contents = conf_file.read()

            conf_complete = re.sub(r"@@(\w+?)@@", lambda match: host[match.group(1)], conf_contents)

            print("LOG: Writing /etc/nginx/conf.d/" + host['hostname'] + ".conf")

            conf_new = open("/etc/nginx/conf.d/" + host['hostname'] + ".conf", "w")
            conf_new.write(conf_complete)
            conf_new.close()

            # cert requests
            if prod=='true':
                os.system("/usr/bin/certbot --nginx --non-interactive --agree-tos --email " + email + " --domain " + host['hostname'])
            else:
                os.system("/usr/bin/certbot --nginx --non-interactive --agree-tos --email " + email + " --domain " + host['hostname'] + " --staging")

        else:
            print("LOG: " + host['hostname'] + " has no proxy_pass, not creating a conf file")

            # cert requests
            if prod=='true':
                os.system("/usr/bin/certbot --nginx --non-interactive --agree-tos --email " + email + " --domain " + host['hostname'])
            else:
                os.system("/usr/bin/certbot --nginx --non-interactive --agree-tos --email " + email + " --domain " + host['hostname'] + " --staging")
    else:
        print("LOG: ERROR: Invalid host, I dont know how this happened")
        quit()
