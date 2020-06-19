FROM python:3.7-buster as builder
LABEL maintainer="sasano8"

RUN pip install --no-cache-dir \
uvicorn \
gunicorn \
poetry

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh

RUN poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project false

ENV PYTHONPATH=/app

EXPOSE 80


COPY ./backend /app
WORKDIR /app/

RUN ls -la
RUN poetry install

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
CMD ["/start.sh"]