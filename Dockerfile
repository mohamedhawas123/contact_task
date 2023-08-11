FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/


RUN pip install --no-cache-dir -r requirements.txt 

COPY . /app/ 

RUN python manage.py collectstatic --noinput



EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "pythonTask.wsgi:application"]


