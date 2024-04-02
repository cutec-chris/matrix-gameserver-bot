FROM python:3.11-alpine as base
FROM base as pybuilder
# RUN sed -i 's|v3\.\d*|edge|' /etc/apk/repositories
RUN apk update && apk add --no-cache olm-dev gcc musl-dev libmagic libffi-dev cmake make g++ git python3-dev
COPY source/requirements.txt /requirements.txt
RUN pip install -U pip setuptools wheel && pip install --user -r /requirements.txt && rm /requirements.txt
FROM base as runner
RUN apk update && apk add --no-cache olm-dev libmagic libffi-dev
COPY --from=pybuilder /root/.local /usr/local
RUN mkdir /bot
RUN mkdir /bot/source
RUN mkdir /data
COPY source/* /bot/source/
RUN pip3 install -r /bot/source/requirements.txt
WORKDIR /data/
CMD [ "python3", "/bot/source/bot.py" ]
