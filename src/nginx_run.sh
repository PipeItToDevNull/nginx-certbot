echo "INFO: Running py file.."
python3 /root/nginx_setup.py & pid1=$!
wait $pid1

echo "INFO: Validating nginx configurations..."
nginx -t

echo "INFO: Setting crontab..."
# set a crontab renewal of certs
SLEEPTIME=$(awk 'BEGIN{srand(); print int(rand()*(3600+1))}'); \
    echo "0 0,12 * * * root sleep $SLEEPTIME && certbot renew -q" | tee -a /etc/crontab > /dev/null

# start crond
crond

if [ -e /var/run/nginx.pid ]; then 
    echo "INFO: nginx is running, finished...";
else 
    nginx -g 'daemon off;';
fi
