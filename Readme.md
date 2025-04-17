# Nginx-Certbot
This container is made from `python:3.11-alpine` with nginx and certbot.

This container allows you to proxy hosts and obtain valid LetsEncrypt certificates with only a JSON string or hand written nginx configuration files.

## Staging
By default the container will fetch [staging](https://letsencrypt.org/docs/staging-environment/) certificates. You must specify `-e PRODUCTION=true` to have the container obtain legitimate certificates. I recommend testing with `-e PRODUCTION=false` first to ensure your setup is working. Testing via the production environment can result in rate limiting or temporary bans from LetsEncrypt servers.

## Example usage
### Simple proxying without pods
```bash
podman network create proxy
```

Add a webserver
```bash
podman run -d --network proxy --name webserver httpd
```

Run the nginx-certbot container
```bash
podman run -d \
    -p 80:80 -p 443:443 \
    -e PRODUCTION=false \
    -e HOSTS='[{"hostname":"contoso.com","proxy_pass":"http://webserver"}]' \
    -e EMAIL=admin@contoso.com \
    --network proxy \
    --name proxy ghcr.io/pipeittodevnull/nginx-certbot:latest
```

### Prefered setup: The proxy is not in a pod while proxying multiple pods
Setup 2 pods and a proxy network
- A shared network between containers is required for DNS resolution and communications. If you have a webserver and a database serving it, only the webserver is put on the proxy network.

```bash
podman pod create web0
podman pod create web1
podman network create proxy
```

Add webservers to the pods(httpd and nginx are used to have a visible difference in the resulting webpages)
```bash
podman run -d --pod web0 --network proxy --name webserver0 httpd
podman run -d --pod web1 --network proxy --name webserver1 nginx
```

Run the nginx-certbot container
```bash
podman run -d \
    -p 80:80 -p 443:443 \
    -e PRODUCTION=false \
    -e HOSTS='[{"hostname":"site0.contoso.com","proxy_pass":"http://web0:8080"},{"hostname":"site1.contoso.com","proxy_pass":"http://web1:8081"}]' \
    -e EMAIL=admin@contoso.com
    --network proxy \
    --name proxy ghcr.io/pipeittodevnull/nginx-certbot:latest
```

### Using manual configuration files
If you have a complex setup that is more than basic ports, such as needing to pass websockets, this would be the method.

Setup 2 pods and a proxy network
- A shared network between containers is required for DNS resolution and communications. If you have a webserver and a database serving it, only the webserver is put on the proxy network.

```bash
podman pod create web0
podman pod create web1
podman network create proxy
```

Add webservers to the pods(httpd and nginx are used to have a visible difference in the resulting webpages)
```bash
podman run -d --pod web0 --network proxy --name webserver0 httpd
podman run -d --pod web1 --network proxy --name webserver1 nginx
```

Configure your site file `conf.d/site.conf` (You can use one file, or put each server in its own)
```
server {
  listen 80;
  server_name site0.contoso.com;
  location / {
      proxy_pass http://web0:8080/;
  }
}
server {
  listen 80;
  server_name site1.contoso.com;
  location / {
      proxy_pass http://web1:8081/;
  }
}
```

Run the nginx-certbot container
```bash
podman run -d \
    -p 80:80 -p 443:443 \
    -v ./conf.d:/etc/nginx/conf.avail \
    -e PRODUCTION=false \
    -e HOSTS='[{"hostname":"site0.contoso.com"},{"hostname":"site1.contoso.com"}]' \
    -e EMAIL=admin@contoso.com
    --network proxy \
    --name proxy ghcr.io/pipeittodevnull/nginx-certbot:latest
```

## Useful docs
- https://www.redhat.com/sysadmin/container-networking-podman

## Building the container
```bash
podman build -t nginx-certbot:latest .
```
