FROM yywzgh/ubuntu:django
LABEL description='Django project for MyWeb'

WORKDIR /app
copy ./django_tools ./django_tools

WORKDIR django_tools/

ENTRYPOINT python3 manage.py runserver