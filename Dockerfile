FROM python:3.8

RUN apt update && apt install -y vim curl gettext

WORKDIR /app/
ADD ./requirements.txt ./requirements.txt

ENV PIP_NO_CACHE_DIR 1
RUN pip install -r ./requirements.txt

ADD ./ ./

CMD ["sh", "-c","./manage.py migrate; ./manage.py compilemessages; ./manage.py collectstatic --noinput; gunicorn --bind=0.0.0.0:8000 --timeout=90 --preload AIC21_Backend.wsgi:application;"]

