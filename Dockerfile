FROM python:3.11-alpine as base

# update os
RUN apk add --no-cache --virtual .build-deps \
        gcc \
        linux-headers \
        openssl-dev \
        musl-dev \
        libffi-dev \
        python3-dev \
        cargo \
        git \
        pkgconfig

# install certbot
RUN python3 -m venv /opt/certbot/ && \
    /opt/certbot/bin/pip install --upgrade pip && \
    /opt/certbot/bin/pip install certbot certbot-nginx && \
    /opt/certbot/bin/pip install pyOpenSSL==23.1.1 && \
    ln -s /opt/certbot/bin/certbot /usr/bin/certbot

# make runtime
FROM python:3.11-alpine as runtime
COPY --from=base /opt/certbot /opt/certbot

RUN apk add --no-cache \
    bash \
    nginx

RUN ln -s /opt/certbot/bin/certbot /usr/bin/certbot 

EXPOSE 80 443

# make the certs in a volume to persist during restarts
VOLUME /etc/letsencrypt

# copy in our execution script
COPY src/* /root/

# healthcheck that isn't useful on podman
HEALTHCHECK --timeout=3s \
  CMD curl -f http://localhost/ || exit 1

# link our logs
RUN ln -sf /dev/stdout /var/log/nginx/access.log && ln -sf /dev/stderr /var/log/nginx/error.log

# start the container process
CMD ["bash","/root/nginx_run.sh"]
