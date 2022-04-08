from python:3.8.0
RUN mkdir /bot
RUN mkdir /bot/source
WORKDIR /bot
COPY source/* /bot/source/
RUN pip3 install -r /bot/source/requirements.txt
CMD [ "python3", "source/bot.py" ]