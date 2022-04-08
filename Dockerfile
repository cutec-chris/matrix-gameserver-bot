from python:3.8.0
RUN mkdir /bot
RUN mkdir /bot/source
RUN mkdir /data
COPY source/* /bot/source/
RUN pip3 install -r /bot/source/requirements.txt
WORKDIR /data/
CMD [ "python3", "/bot/source/bot.py" ]
