from init import *
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
try:
    with open('data.json', 'r') as f:
        servers = json.load(f)
except: pass
bot.run()