# matrix-gameserver-bot

A bot to access game console over an rcon port. 
You can send commands to your game server from an matrix channel.
To show game details also Steam A2S Query Port is supported

## Setup

copy config.sample.yml to config.yml and fill out username an apsswort from an existing matrix user for the bot.
you can also edit the prefix on wich the bot reacts.

## Usage

Invite the bot to an channel and add an server there with the listen command.
Commands are described by the help command.

Messages to the Bot (to prefix) are used as rcon console command. 
Messages in the channel are shown as global chat if supported.

## tested Games

* ARK Survival Evolved

### untested
* CS:GO
* Minecraft
* [Conan Exiles](https://store.steampowered.com/app/440900/Conan_Exiles/)
* Reign Of Kings