This container is made from UBI8 with nginx and certbot installed via pip.

You are required to mount valid nginx http configurations, these are copied at runtime so they are not over-written on disk.

You are required to include all `server_name`'s in the `VIRTUAL_HOSTNAMES` env var, they are comma delimitted in a single variable. `EMAIL` is the administrative email registered with LetsEncrypt for your domain.

## Examples
### Proxying without pods
```bash
sudo podman network create web
```

Add a webserver
```bash
sudo podman run -d --network web --name webserver httpd
```

Configure your site file `conf.d/site.conf` (the conf name is inconsequential)
```
server {
  listen 80;
  server_name contoso.com;
  location / {
      proxy_pass http://webserver/;
  }
}
```

Run the nginx-certbot container
```bash
sudo podman run -d -it \
    -p 80:80 -p 443:443 \
    -v ./conf.d:/etc/nginx/conf.avail \
    -e VIRTUAL_HOSTNAMES=contoso.com \
    -e EMAIL=admin@contoso.com
    --network web \
    --name proxy nginx-certbot
```

### Prefered setup: The proxy is not in a pod while proxying multiple pods
Setup 2 pods and a proxy network
- A shared network between containers is required for DNS resolution and communications. If you have a webserver and a database serving it, only the webserver is put on the proxy network.
```bash
sudo podman pod create web0
sudo podman pod create web1
sudo podman network create proxy
```

Add webservers to the pods(httpd and nginx are used to have a visible difference in the resulting webpages)
```bash
sudo podman run -d --pod web0 --network proxy --name webserver0 httpd
sudo podman run -d --pod web1 --network proxy --name webserver1 nginx
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
sudo podman run -d -it \
    -p 80:80 -p 443:443 \
    -v ./conf.d:/etc/nginx/conf.avail \
    -e VIRTUAL_HOSTNAMES=site0.contoso.com,site1.contoso.com \
    -e EMAIL=admin@contoso.com
    --network proxy \
    --name proxy nginx-certbot
```

## Staging
`nginx_run.sh` is executed in the container, this contains `--staging` in the certbot command. Once you know your setup works remove this argument to retrieve valid certificates from LetsEncrypt instead of invalid staging certificates.

## Useful docs
- https://www.redhat.com/sysadmin/container-networking-podman
