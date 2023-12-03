import os
import json
import re
import logging

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

# Take the env var and make it an object (A list of dictionaries)
hosts_var = os.getenv('HOSTS')
hosts_json = json.loads(hosts_var)

email = os.getenv('EMAIL')
prod = os.getenv('PRODUCTION')

# copy in any manual conf files the user made
os.system("cp -rf /etc/nginx/conf.avail/*.conf /etc/nginx/conf.d/ &> /dev/null")
logging.info("Configurations present: " + str(os.listdir("/etc/nginx/conf.d")))

# Basic log printing
logging.info("Found: " + str(len(hosts_json)) + " hosts")

for host in hosts_json:
    for key, value in host.items():
        logging.info(f"Found: {key}:{value}")

for host in hosts_json:
    logging.info("Working on: " + host['hostname'])

    if "hostname" in host:
        logging.info(host['hostname'] + " is valid")

        if "proxy_pass" in host:
            logging.info(host['hostname'] + " has proxy_pass " + host['proxy_pass'] + " creating conf file")

            # configuration file creation
            with open('/root/skel.conf') as conf_file:
                conf_contents = conf_file.read()

            conf_complete = re.sub(r"@@(\w+?)@@", lambda match: host[match.group(1)], conf_contents)

            logging.info("Writing /etc/nginx/conf.d/" + host['hostname'] + ".conf")

            conf_new = open("/etc/nginx/conf.d/" + host['hostname'] + ".conf", "w")
            conf_new.write(conf_complete)
            conf_new.close()

            # cert requests
            if prod=='true':
                os.system("/usr/bin/certbot --nginx --non-interactive --agree-tos --email " + email + " --domain " + host['hostname'])
            else:
                os.system("/usr/bin/certbot --nginx --non-interactive --agree-tos --email " + email + " --domain " + host['hostname'] + " --staging")

        else:
            logging.info(host['hostname'] + " has no proxy_pass, not creating a conf file")

            # cert requests
            if prod=='true':
                os.system("/usr/bin/certbot --nginx --non-interactive --agree-tos --email " + email + " --domain " + host['hostname'])
            else:
                os.system("/usr/bin/certbot --nginx --non-interactive --agree-tos --email " + email + " --domain " + host['hostname'] + " --staging")
    else:
        logging.error("Invalid host, I dont know how this happened")
        quit()
