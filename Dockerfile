FROM redhat/ubi8-minimal

# update os
RUN microdnf update -y && microdnf install -y python3-virtualenv augeas-libs nginx cronie && microdnf clean all

# install certbot
RUN python3 -m venv /opt/certbot/ && \
    /opt/certbot/bin/pip install --upgrade pip && \
    /opt/certbot/bin/pip install certbot certbot-nginx && \
    /opt/certbot/bin/pip install pyOpenSSL==23.1.1 && \
    ln -s /opt/certbot/bin/certbot /usr/bin/certbot

# make the certs in a volume to persist during restarts
VOLUME /etc/letsencrypt

# copy in our execution script
COPY src/* /root/

# healthcheck that isn't useful on podman
HEALTHCHECK --timeout=3s \
  CMD curl -f http://localhost/ || exit 1

# redirect nginx logs
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80 443

# start the container process
CMD ["bash","/root/nginx_run.sh"]
