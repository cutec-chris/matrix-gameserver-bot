from python:alpine
RUN mkdir /bot
RUN mkdir /bot/source
WORKDIR /bot
COPY source/* /bot/source/
RUN pip install -r /bot/source/requirements.txt
CMD [ "python", "source/bot.py" ]