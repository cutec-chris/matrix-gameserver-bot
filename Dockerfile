from python:alpine
mkdir /bot
WORKDIR /bot
copy source/* /bot/
run pip install -r /bot/requirements.txt
CMD [ "python", "bot.py" ]