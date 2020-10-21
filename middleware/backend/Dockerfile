FROM sasano8/basic_fastapi_selenium-standalone-chrome-debug:3.8 as builder
LABEL maintainer="sasano8"


USER root

ENV PYTHONPATH=/app

EXPOSE 80
EXPOSE 8080
EXPOSE 5672
EXPOSE 22

RUN sudo apt-get update && sudo apt install -y openssh-server && sudo apt install -y vim
RUN sudo mkdir /run/sshd

RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
# COPY ./config_files/id_rsa.pub /root/.ssh/authorized_keys
RUN echo "root:secret" | chpasswd

ARG UID=1000
ARG GID=1000

RUN usermod -u $UID seluser
RUN groupmod -g $GID seluser
RUN usermod -aG root seluser
USER seluser

COPY ./app/pyproject.toml /app/pyproject.toml
COPY ./app/poetry.lock* /app/
WORKDIR /app/

COPY ./start.sh /start.sh
RUN sudo chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN sudo chmod +x /start-reload.sh

COPY ./start_celery_worker.sh /start_celery_worker.sh
RUN sudo chmod +x /start_celery_worker.sh

COPY ./app /app
RUN ls -la

COPY ./supervisor/fastapi.conf /etc/supervisor/conf.d/
COPY ./supervisor/celery_worker.conf /etc/supervisor/conf.d/
COPY ./supervisor/sshd.conf /etc/supervisor/conf.d/

# Run the start script, it will check for an /app/prestart.sh script (e.g. for migrations)
# And then will start Gunicorn with Uvicorn
# ENV IS_WORKER
# CMD ["/start.sh", "$IS_WORKER"]
# CMD /start.sh $IS_WORKER


RUN sudo pip3 install --upgrade keyrings.alt


# python3.6.9の場合、以下のパッケージが入れないと動かない
# RUN sudo pip install dataclasses

# sudoをつけないと、poetryがグローバルインストールされているため権限エラーが発生する
RUN sudo apt install -y graphviz libgraphviz-dev  # eralchemyのer出力にグラフライブラリが必要
# RUN sudo poetry update
RUN sudo poetry install


# /opt/bin　実行するシェル
# /etc/supervisor/conf.d/ デーモンの定義


