echo "Copying configs..."
cp -rf --verbose /etc/nginx/conf.avail/* /etc/nginx/conf.d
echo "Running certbot..."

# request our certificates
for host in $(echo $VIRTUAL_HOSTNAMES | tr "," "\n"); \
    do /usr/bin/certbot --nginx \
        --non-interactive \
        --agree-tos --email $EMAIL \
        --domain $host --staging ; \
done

# set a crontab renewal of certs
SLEEPTIME=$(awk 'BEGIN{srand(); print int(rand()*(3600+1))}'); \
    echo "0 0,12 * * * root sleep $SLEEPTIME && certbot renew -q" | tee -a /etc/crontab > /dev/null

# start crond
crond

if [ -e /var/run/nginx.pid ]; then 
    echo "nginx is running";
else 
    nginx -g 'daemon off;';
fi
