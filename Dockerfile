FROM python:3.9.7-buster
WORKDIR /code
COPY ./movies_admin/requirements.txt /code
RUN pip install -r /code/requirements.txt --no-cache-dir
COPY ./movies_admin /code
CMD ["gunicorn", "config.wsgi", "--preload", "--bind", "0.0.0.0:8000"]
