from python:alpine
mkdir /bot
mkdir /bot/source
WORKDIR /bot
copy source/* /bot/source/
run pip install -r /bot/source/requirements.txt
CMD [ "python", "source/bot.py" ]