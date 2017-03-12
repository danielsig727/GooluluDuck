FROM python:2.7-alpine

RUN echo '@testing http://nl.alpinelinux.org/alpine/edge/testing'>>/etc/apk/repositories && \
    apk update && apk add opencc@testing

RUN mkdir -p /root/slackbot
COPY *.py requirements.txt /
RUN echo '{}' > /emotibot_userid_db.json
RUN cd /root/slackbot && pip install -r /requirements.txt
RUN ln -s /usr/lib/libopencc.so.1.0.0 /usr/lib/libopencc.so.1

CMD ["python2", "/slackbot_run.py"]
