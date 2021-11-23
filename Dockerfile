FROM python:3.9.0-buster
RUN printf 'deb http://nginx.org/packages/debian/ buster nginx\n' > /etc/apt/sources.list.d/nginx.list  && \
    curl -sL 'http://nginx.org/keys/nginx_signing.key' | apt-key add  - && \
    apt-get update && \
    apt-get install -fy build-essential nginx tini && \
    pip install --upgrade pip && \
    mkdir -p src/python

EXPOSE 8080
ENV TINI_SUBREAPER="true"
ENV DEBUG=False

COPY requirements.txt /opt/
RUN  pip install -r /opt/requirements.txt

COPY alarmbutton_backend/ /opt/

COPY run.sh /opt/
RUN chmod +x /opt/run.sh
WORKDIR /opt/


COPY nginx-config /etc/

#RUN './run.sh'
ENTRYPOINT ["/opt/run.sh"]