from init import *
import rcon
servers = []

@bot.listener.on_message_event
async def listen(room, message):
    match = botlib.MessageMatch(room, message, bot, prefix)
    if match.is_not_from_this_bot() and match.prefix()\
    and match.command("listen"):
        server = {
            'room': room.room_id,
            'server': match.args()[1],
            'port': match.args()[2],
            'password': match.args()[3],
        }
        servers.append(server)
        with open('data.json', 'w') as f:
            json.dump(servers,f)
        await bot.api.send_text_message(room.room_id, 'server added')
@bot.listener.on_message_event
async def bot_help(room, message):
    bot_help_message = f"""
    Help Message:
        prefix: {prefix}
        commands:
            listen:
                command: listen server port password
                description: add ark server
            help:
                command: help, ?, h
                description: display help command
                """
    match = botlib.MessageMatch(room, message, bot, prefix)
    if match.is_not_from_this_bot() and match.prefix() and (
       match.command("help") 
    or match.command("?") 
    or match.command("h")):
        await bot.api.send_text_message(room.room_id, bot_help_message)
async def check_server(server,room):
    while True:
        with rcon.source.Client(server['server'], int(server['port']), passwd=server['password']) as client:
            room.arkclient = None
            def tell(*args):
                res = client.run(*args)
                #print(*args)
                if not 'Server received, But no response!!' in res:
                    return res
                return None
            def ShowGameLog(room):
                res = tell('GetGameLog')
                if res:
                    room.send_text(res)
                    print(res)
                    res = res.split('\n')
            room.send_text('Server '+map+' is up now...')
            room.arkclient = client
            room.docker = docker
            room.add_listener(on_message)
            ConnectionDone = True
            while True:
                ShowGameLog(room)
@bot.listener.on_startup
def startup(server):
    try:
        with open('data.json', 'r') as f:
            servers = json.load(f)
    except: pass
    loop = asyncio.get_event_loop()
    for server in servers:
        loop.create_task(check_server(server,''))
bot.run()