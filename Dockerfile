from python:alpine
RUN mkdir /bot
RUN mkdir /bot/source
WORKDIR /bot
COPY source/* /bot/source/
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /bot/source/requirements.txt
RUN apk del .tmp-build-deps
CMD [ "python", "source/bot.py" ]