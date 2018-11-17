# django-apache-nginx-uwsgi-vps-ubuntu
Tutorial on how to deploy a Django application on Linux VPS with Apache, NGINX and uWSGI

## Preparing the environmnet
* Create virtual env

```python3 -m venv venv```

* Clone repository

```git clone your-url.git```

 ## Setup static and media files
 
 * Make sure your settings.py has the following configurations:
 ```
 STATIC_URL = '/static/'
 STATIC_ROOT = os.path.join(BASE_DIR, "static")
 
 MEDIA_URL = '/media/'
 MEDIA_ROOT = os.path.join(BASE_DIR, "media")
 ```
 
 * Run Django collectstatic
 ```python manage.py collectstatic```

 
 ## Install and setup 
 * Install uwsgi on your virtual environment
 
 ```pip install uwsgi```

* Install and start Nginx

```
sudo apt-get install nginx
sudo /etc/init.d/nginx start
```
## Configure Nginx

```
upstream django {
    server unix:///path/to/your/mysite/mysite.sock; # for a file socket
}

server {
    listen      8000;
    server_name example.com;
    charset     utf-8;

    client_max_body_size 75M;   # adjust to taste

    location /media  {
        alias /path/to/your/mysite/media; 
    }

    location /static {
        alias /path/to/your/mysite/static;
    }

    location / {
        uwsgi_pass  django;
        include     /path/to/your/mysite/uwsgi_params; 
    }
}
```

* Create a symlink on sites-enabled
sudo ln -s ~/path/to/your/mysite/mysite_nginx.conf /etc/nginx/sites-enabled/

* Restart Nginx
```sudo /etc/init.d/nginx restart```

* Download an image to media folder and test

* Run and test using Unix sockets
```uwsgi --socket mysite.sock --module mysite.wsgi --chmod-socket=666```

* Create the ini file

```[uwsgi]
chdir           = /home/ubuntu/gestao_rh
module          = gestao_rh.wsgi
home            = /home/ubuntu/venv
master          = true
processes       = 10
socket          = /home/ubuntu/gestao_rh/mysite.sock
vacuum          = true
chmod-socket    = 666
```

* Testing with .ini file
```uwsgi --ini mysite_uwsgi.ini```


## Configuring the uWSGI as Emperor mode
```
sudo mkdir /etc/uwsgi
sudo mkdir /etc/uwsgi/vassals
sudo ln -s /path/to/your/mysite/mysite_uwsgi.ini /etc/uwsgi/vassals/
uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data
```
## Setup systemctl to start on boot

```
https://uwsgi-docs.readthedocs.io/en/latest/Systemd.html

/etc/systemd/system/

sudo vim uwsgi_gestao_rh.service


======
[Unit]
Description=uWSGI Emperor
After=syslog.target

[Service]
ExecStart=/home/ubuntu/venv/bin/uwsgi --emperor /etc/uwsgi/vassals --uid www-data --gid www-data
RuntimeDirectory=uwsgi
Restart=always
KillSignal=SIGQUIT
Type=notify
StandardError=syslog
NotifyAccess=all
User=ubuntu

[Install]
WantedBy=multi-user.target
======

sudo chmod 664 /etc/systemd/system/uwsgi_gestao_rh.service

sudo systemctl daemon-reload

sudo systemctl enable uwsgi_gestao_rh.service

 sudo systemctl start uwsgi_gestao_rh.service

 sudo systemctl status uwsgi_gestao_rh.service

journalctl -u uwsgi_gestao_rh.service

```
