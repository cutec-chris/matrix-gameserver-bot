from init import *
import rcon,a2s
loop = None
lastsend = None
class Server(Config):
    def __init__(self, room, **kwargs) -> None:
        super().__init__(room, **kwargs)
@bot.listener.on_message_event
async def tell(room, message):
    global servers,lastsend
    match = botlib.MessageMatch(room, message, bot, prefix)
    if match.is_not_from_this_bot() and match.prefix()\
    and match.command("listen"):
        server = Server({
            'room': room.room_id,
            'server': match.args()[1],
            'rcon': match.args()[2],
            'password': None
        })
        if len(match.args())>3:
            server.password = match.args()[3]
        if len(match.args())>4:
            server.qport = match.args()[4]
        servers.append(server)
        loop.create_task(check_server(server))
        with open('data.json', 'w') as f:
            json.dump(servers,f, skipkeys=True)
        await bot.api.send_text_message(room.room_id, 'ok')
    elif match.is_not_from_this_bot() and match.prefix():
        for server in servers:
            if server.room == room.room_id and '_client' in server:
                break
        if server.room != room.room_id: return
        ncmd = " ".join(arg for arg in match.args())
        if not ('admins' in server and message.sender in server.admins):
            await bot.api.send_text_message(room.room_id, 'not authorized')
        try:
            res = server._client.run(ncmd)
            if not 'Server received, But no response!!' in res:
                await bot.api.send_text_message(room.room_id, res)
        except BaseException as e:
            await bot.api.send_text_message(room.room_id, str(e))
    elif match.is_not_from_this_bot():
        for server in servers:
            if server.room == room.room_id and '_client' in server:
                break
        if server.room != room.room_id: return
        try:
            user = message.sender
            user = user[:user.find(':')]
            if user[:1] == '@':
                user = user[1:]
            server._client.run('ServerChat',user+':'+message.body)
            server._client.run('amx_say',user+':'+message.body)
            lastsend = user+':'+message.body
        except:
            pass
async def check_server(server):
    global lastsend,servers
    while True:
        try:
            with rcon.source.Client(server.server, int(server.rcon), passwd=server.password) as client:
                server._client = client
                #update_server_var()
                def tell(*args):
                    res = client.run(*args)
                    #print(*args)
                    if not 'Server received, But no response!!' in res:
                        return res
                    return None
                try:
                    info = a2s.info((server.server, int(server.qport)))
                    answer = 'Server %s is up with %s ...\nMap: %s\nPlayers: %d of %d' % (info.server_name,info.game,info.map_name,info.player_count,info.max_players)
                except BaseException as e:
                    info = None
                    answer = 'Server is up now...'
                await bot.api.send_text_message(server.room,answer)
                res = tell('GetGameLog')
                if not 'error' in str(res):
                    server.gamelog = True
                while True:
                    res = None
                    if hasattr(server,'gamelog') and server.gamelog:
                        res = tell('GetGameLog')
                    if res:
                        if 'error' in str(res):
                            server.gamelog = False
                            #update_server_var()
                        res = res[res.find(':')+1:].rstrip()
                        if 'SERVER:' in res:
                            res = res[res.find(':')+1:]
                        if not lastsend or (not (lastsend in res)):
                            await bot.api.send_text_message(server.room,res)
                        else:
                            lastsend = None
                    else:
                        await asyncio.sleep(0.3)
        except BaseException as e:
            if not hasattr(server,'lasterror') or server.lasterror != str(e):
                await bot.api.send_text_message(server.room,str(server.server)+': '+str(e))
                server.lasterror = str(e)
        await asyncio.sleep(5)
try:
    with open('data.json', 'r') as f:
        nservers = json.load(f)
        for server in nservers:
            servers.append(Server(server))
except BaseException as e: 
    logging.error('Failed to read config.yml:'+str(e))
    exit(1)
@bot.listener.on_startup
async def startup(room):
    global loop,servers
    loop = asyncio.get_running_loop()
    for server in servers:
        if server.room == room:
            loop.create_task(check_server(server))
@bot.listener.on_message_event
async def bot_help(room, message):
    bot_help_message = f"""
    Help Message:
        prefix: {prefix}
        commands:
            speaking to bot:
                is used as rcon console command when you are in the admins list
            speaking in channel:
                is send as server global chat message if supported
            listen:
                command: listen server rcon_port [password] [Query Port]
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