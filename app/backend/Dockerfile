FROM sasano8/basic_fastapi_selenium-standalone-chrome-debug as builder
LABEL maintainer="sasano8"

USER root

ENV PYTHONPATH=/app

EXPOSE 80
EXPOSE 8080
EXPOSE 5672
EXPOSE 22

RUN sudo apt install -y openssh-server
RUN sudo mkdir /run/sshd




COPY ./backend/pyproject.toml /app/pyproject.toml
COPY ./backend/poetry.lock* /app/
WORKDIR /app/

# python3.6.9の場合、以下のパッケージが入れないと動かない
RUN pip install dataclasses

RUN ls -la
RUN poetry install

COPY ./start.sh /start.sh
RUN sudo chmod +x /start.sh
# RUN sudo chown seluser:seluser /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py
# RUN sudo chown seluser:seluser /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN sudo chmod +x /start-reload.sh
# RUN sudo chown seluser:seluser /start-reload.sh

COPY ./start_celery_worker.sh /start_celery_worker.sh
RUN sudo chmod +x /start_celery_worker.sh

COPY ./backend /app
RUN ls -la
# ONBUILD COPY ./backend /app

# RUN sudo chown -R seluser:seluser /app

COPY ./supervisor/fastapi.conf /etc/supervisor/conf.d/
COPY ./supervisor/celery_worker.conf /etc/supervisor/conf.d/
COPY ./supervisor/sshd.conf /etc/supervisor/conf.d/

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
# ENV IS_WORKER
# CMD ["/start.sh", "$IS_WORKER"]
# CMD /start.sh $IS_WORKER


RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
# COPY ./config_files/id_rsa.pub /root/.ssh/authorized_keys
RUN echo "root:secret" | chpasswd

# /opt/bin　実行するシェル
# /etc/supervisor/conf.d/ デーモンの定義


