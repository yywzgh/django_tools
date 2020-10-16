FROM yywzgh/ubuntu:django
LABEL description='Django project for MyWeb'

WORKDIR /app
copy ./MyWeb ./myweb

WORKDIR myweb/

ENTRYPOINT python3 manage.py runserver