# My Innerapps API
==========================

## Table of content
- [Prerequisites](#prerequisites)
- [Project config](#project-configuration)
- [Dev Server](#dev-server)

## Prerequisites

The prerequisites are Git, Python3 and pip3.

https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/

https://linuxize.com/post/how-to-create-python-virtual-environments-on-ubuntu-18-04/

We need to create a virtualenv:

```
$ sudo apt install python3-venv
$ cd
$ mkdir .envs
$ cd .envs
$ python3 -m venv <my-project-env>
$ source <my-project-env>/bin/activate
```

## Project config

En primer lugar hay que descargarse el repositorio del projecto en el lugar deseado.
Firstly, you must clonate the repository:

```sh
$ git clone https://innersource.soprasteria.com/innerapps/my-innerapps-api.git
$ cd my-innerapps-api
```

with the virtualenv created, install requirements:

```
(my-project-env) $ pip install -r requirements.txt
```

Environment configuration:
You must set an environment variable in the OS to select the correct configuration:
```
local env: DJANGO_SETTINGS_MODULE=my_innerapps_api.settings.local
dev env: DJANGO_SETTINGS_MODULE=my_innerapps_api.settings.dev
prod env: env var no needed
```

Then, up the server:
```
(my-project-env) $ python manage.py migrate
(my-project-env) $ python manage.py createsuperuser
(my-project-env) $ python manage.py runserver
```

Load fixtures:
```
(my-project-env) $ python manage.py loaddata people
```

Database file for local development:
```
/my-innerapps-api/my_innerapps_api/db.sqlite3
```

In browser, navigate to http://127.0.0.1:8000

### Available URL's:
- Django administration:

    - http://127.0.0.1:8000/admin/

- Swagger:

    - http://127.0.0.1:8000/api/docs/

- API:

    - http://127.0.0.1:8000/api/rest-auth/login/ (return authentication token with username and password fields)
    - http://127.0.0.1:8000/api/v1/people/ (return all collaborators, need to send a valid token)
    - http://127.0.0.1:8000/api/v1/people/1/ (to work with collaborato with id=1, need to send a valid token too)
    - The authentication token is set in header: 'Authorization=Token xxxxxxxxxxxxxxxxx'

## Dev Server:

### Digital Ocean Server

    - IP: 165.227.141.114
    - username: root
    - password: innerapps1234
    - folder: /home/my-innerapps/my-innerapps-api/
    - virtual env activation: /home/my-innerapps/my-innerapps-api/source myinnerappsapienv/bin/activate
    - Gunicorn
        - Configuration file: /etc/systemd/system/gunicorn.service
        - Restart:
            - sudo systemctl daemon-reload
            - sudo systemctl restart gunicorn
    - Nginx
        - Configuration file: /etc/nginx/sites-available/myinnerappsapi
        - Restart: sudo systemctl restart nginx
    - Supervisord
        - Configuration file: /etc/supervisor/conf.d/my-innerapps-api.conf
        - Restart: sudo service supervisor restart

    - REST API URL:
        - http://165.227.141.114:8081

    - POSTGRESQL:
        - host=165.227.141.114
        - port=5432
        - username=admin
        - password=wxkt56YF3

### Deploy Procedure

    - Manual:
        $ ssh root@165.227.141.114
        $ cd /home/my-innerapps/my-innerapps-api/
        $ source myinnerappsapienv/bin/activate
        (myinnerappsapienv) $ git checkout <branch_to_deploy>
        (myinnerappsapienv) $ git pull
        (myinnerappsapienv) $ python manage.py migrate
        (myinnerappsapienv) $ python manage.py collectstatic
        $ sudo service supervisor restart
        $ sudo systemctl daemon-reload
        $ sudo systemctl restart gunicorn
        $ sudo nginx -t
        $ sudo systemctl restart nginx

    - Automatic:
        -  Install ansible in your machine just once:
            $ sudo apt update
            $ sudo apt install software-properties-common
            $ sudo apt-add-repository ppa:ansible/ansible
            $ sudo apt update
            $ sudo apt install ansible

        -  Execute deploy command:
            $ cd ansible
            $ ./ansible.sh deploy.yml dev



