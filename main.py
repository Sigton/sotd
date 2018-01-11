import discord
import asyncio
import logging
import datetime
import time
import json

logging.basicConfig(level=logging.INFO)
client = discord.Client()

post_logs = {}

with open("post_log.json", "r") as f:
    post_logs = json.load(f)

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

@client.event
async def on_message(message):

    global post_logs

    # m0add
    if message.content.startswith("m0add"):
        args = message.content.split(" ")[1:]

        with open("post_log.json", "r") as f:
            post_logs = json.load(f)
        
        if not len(args):
            await client.send_message(message.channel, "You think you're smart tryna trick me. Put a song in next time.")
            return

        if (not args[0][0:32] == "https://www.youtube.com/watch?v=") and (not args[0][0:17] == "https://youtu.be/"):
            await client.send_message(message.channel, "That ain't a youtube video. Try again.")
            return

        if args[0] in post_logs["ban_songs"]:
            await client.send_message(message.channel, "Nice try, but we heard that one enough.")
            return

        if message.author.id not in list(post_logs["post_log"].keys()):
            post_logs["post_log"][message.author.id] = time.time()
        else:
            if time.time() - post_logs["post_log"][message.author.id] >= 64800:
                post_logs["post_log"][message.author.id] = time.time()
            else:
                await client.send_message(message.channel, "It's song of the DAY not song of the minute. Geez.")
                return

        username = message.author.nick
        if username is None:
            username = message.author.name
            
        song_channel = [channel for channel in message.server.channels if "song" in channel.name][0]
        
        await client.send_message(song_channel, """Song of the Day {} ({})
~~                                                                              ~~
{}""".format(datetime.datetime.today().strftime('%Y-%m-%d'), username, args[0]))

        with open("post_log.json", "w") as f:
            post_logs = json.dump(post_logs, f)

        return

    # m0ban
    if message.content.startswith("m0ban"):

        with open("post_log.json", "r") as f:
            post_logs = json.load(f)
        
        args = message.content.split(" ")[1:]

        if "Admins" not in [role.name for role in message.author.roles]:
            await client.send_message(message.channel, "Don't touch that. <:angertivity:394473102769258497>")
            return

        if not len(args):
            await client.send_message(message.channel, "You need to tell me which song to ban, im not psychic!")
            return

        if (not args[0][0:32] == "https://www.youtube.com/watch?v=") and (not args[0][0:17] == "https://youtu.be/"):
            await client.send_message(message.channel, "That ain't a youtube video.")
            return

        if args[0] in post_logs["ban_songs"]:
            await client.send_message(message.channel, "No need to ban it twice.")
            return

        post_logs["ban_songs"].append(args[0])

        await client.send_message(message.channel, "That's the last we'll see of that song!")

        with open("post_log.json", "w") as f:
            post_logs = json.dump(post_logs, f)
        
        return

client.run("secret")
