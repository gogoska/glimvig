FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /site

COPY requirements/production.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY glimvig/ .

RUN python manage.py collectstatic --noinput

RUN adduser --disabled-password django-user

USER django-user

EXPOSE 8000

CMD ["gunicorn", "glimvig.wsgi:application", "--bind", "0.0.0.0:8000"]"