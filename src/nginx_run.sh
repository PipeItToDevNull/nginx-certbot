echo "INFO: Running py file.."
python3 /root/nginx_setup.py & pid1=$!
wait $pid1

if [ $pid1 -ne 0 ]; then
    echo "Setup failed, terminating"
    exit 1
fi

echo "INFO: Validating nginx configurations..."
nginx -t

echo "INFO: Setting crontab..."
# set a crontab renewal of certs
SLEEPTIME=$(awk 'BEGIN{srand(); print int(rand()*(3600+1))}'); \
    echo "0 0,12 * * * sleep $SLEEPTIME && if certbot renew -q; then echo 'certbot renewed' >> /proc/1/fd/1; else echo 'certbot error' >> /proc/1/fd/2; fi" | crontab -

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
