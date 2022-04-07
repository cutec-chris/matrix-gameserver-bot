from python:alpine
mkdir /bot
copy source/* /bot/
run pip install -r /bot/requirements.txt