echo "INFO: Running py file.."
python3 /root/nginx_setup.py & pid1=$!
wait $pid1

echo "INFO: Validating nginx configurations..."
nginx -t

echo "INFO: Setting crontab..."
# set a crontab renewal of certs
SLEEPTIME=$(awk 'BEGIN{srand(); print int(rand()*(3600+1))}'); \
    echo "0 0,12 * * * root sleep $SLEEPTIME && certbot renew -q && echo 'cerbot renewed' > /dev/stdout" | crontab -

# start crond
crond -d 2

# restart nginx
nginx -s stop

while [ -e /var/run/nginx.pid ]; do
    echo "INFO: Waiting for nginx process... "
    sleep 1
done

echo "INFO: Starting nginx..."
exec nginx -g 'daemon off;'
