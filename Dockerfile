FROM python:3.9

LABEL maintainer = "chikovm@bk.ru"
LABEL description="For Dj-prj"

ENV PYTHONUNBUFFERED 'on'

WORKDIR /code

COPY requirements.txt /code/
COPY .dockerignore 

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]