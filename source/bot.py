from init import *
import rcon,a2s
servers = []
loop = None
lastsend = None
@bot.listener.on_message_event
async def listen(room, message):
    global servers
    match = botlib.MessageMatch(room, message, bot, prefix)
    if match.is_not_from_this_bot() and match.prefix():
        for server in servers:
            if server['room'] == room.room_id:
                break
        if server['room'] != room.room_id: return
        ncmd = " ".join(arg for arg in match.args())
        if not ('admins' in server and message.sender in server['admins']):
            await bot.api.send_text_message(room.room_id, 'not authorized')
        try:
            res = server['_client'].run(ncmd)
            if not 'Server received, But no response!!' in res:
                await bot.api.send_text_message(room.room_id, res)
        except BaseException as e:
            await bot.api.send_text_message(room.room_id, str(e))
@bot.listener.on_message_event
async def listen(room, message):
    global servers,lastsend
    match = botlib.MessageMatch(room, message, bot, prefix)
    if match.is_not_from_this_bot():
        for server in servers:
            if server['room'] == room.room_id:
                break
        if server['room'] != room.room_id: return
        try:
            user = message.sender
            user = user[:user.find(':')]
            if user[:1] == '@':
                user = user[1:]
            server['_client'].run('ServerChat',user+':'+message.body)
            lastsend = user+':'+message.body
        except:
            pass
async def check_server(server):
    global lastsend
    while True:
        try:
            with rcon.source.Client(server['server'], int(server['rcon']), passwd=server['password']) as client:
                server['_client'] = client
                def tell(*args):
                    res = client.run(*args)
                    #print(*args)
                    if not 'Server received, But no response!!' in res:
                        return res
                    return None
                try:
                    info = a2s.info((server['server'], int(server['qport'])))
                    answer = 'Server %s is up with %s ...\nMap: %s\nPlayers: %d of %d' % (info.server_name,info.game,info.map_name,info.player_count,info.max_players)
                except BaseException as e:
                    info = None
                    answer = 'Server is up now...'
                await bot.api.send_text_message(server['room'],answer)
                while True:
                    res = tell('GetGameLog')
                    if res:
                        res = res[res.find(':')+1:].rstrip()
                        if 'SERVER:' in res:
                            res = res[res.find(':')+1:]
                        if not lastsend or (not (lastsend in res)):
                            await bot.api.send_text_message(server['room'],res)
                        else:
                            lastsend = None
                    else:
                        await asyncio.sleep(0.3)
        except BaseException as e:
            if 'Connection' in str(e): pass
            else:
                await bot.api.send_text_message(server['room'],str(e))
        await asyncio.sleep(5)
@bot.listener.on_startup
async def startup(room):
    global loop,servers
    loop = asyncio.get_running_loop()
    try:
        with open('data.json', 'r') as f:
            servers = json.load(f)
    except: pass
    for server in servers:
        if server['room'] == room:
            loop.create_task(check_server(server))
@bot.listener.on_message_event
async def listen(room, message):
    match = botlib.MessageMatch(room, message, bot, prefix)
    if match.is_not_from_this_bot() and match.prefix()\
    and match.command("listen"):
        server = {
            'room': room.room_id,
            'server': match.args()[1],
            'qport': match.args()[2],
            'rcon': match.args()[3],
            'password': match.args()[4],
        }
        servers.append(server)
        loop.create_task(check_server(server))
        with open('data.json', 'w') as f:
            json.dump(servers,f, skipkeys=True)
        await bot.api.send_text_message(room.room_id, 'ok')
@bot.listener.on_message_event
async def bot_help(room, message):
    bot_help_message = f"""
    Help Message:
        prefix: {prefix}
        commands:
            listen:
                command: listen server query_port rcon_port password
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
bot.run()