import simplematrixbotlib as botlib,yaml,json,asyncio
with open('config.yml', 'r') as file:
    config = yaml.safe_load(file)
try: 
    prefix = config['server']['prefix']
except:
    prefix = config['server']['user']
creds = botlib.Creds(config['server']['url'], config['server']['user'], config['server']['password'])
bot = botlib.Bot(creds)