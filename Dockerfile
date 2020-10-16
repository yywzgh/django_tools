FROM yywzgh/ubuntu:django
LABEL description='Django project for MyWeb'

RUN mkdir /tmp/upload
RUN mkdir /tmp/data

WORKDIR /app
copy ./django_tools ./django_tools

WORKDIR django_tools/

ENTRYPOINT python3 manage.py runserver