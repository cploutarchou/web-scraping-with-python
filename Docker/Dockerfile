FROM ubuntu:16.04
RUN apt-get update && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && apt-get install -y python3.6 python3.6-dev python3-pip

RUN ln -sfn /usr/bin/python3.6 /usr/bin/python3 && ln -sfn /usr/bin/python3 /usr/bin/python && ln -sfn /usr/bin/pip3 /usr/bin/pip
COPY Docker/requirements.txt /tmp/
COPY app /app/
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt
# Install cron
RUN apt-get update && apt-get install -y cron

ADD scripts/entrypoint.sh /entrypoint.sh

RUN chmod +x  /entrypoint.sh

ENTRYPOINT /entrypoint.sh