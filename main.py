import os
import discord
from dotenv import load_dotenv
from googlesearch import search
import psycopg2
# from flask import Flask
# from os import environ
#
#
# app = Flask(__name__)
# app.run(environ.get('PORT'))

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

connection = psycopg2.connect(user="postgres",
                              password="kirti@@1",
                              host="127.0.0.1",
                              port="5432",
                              database="bs_db")


cursor = connection.cursor()

client = discord.Client()

@client.event
async def on_ready():
    # str= "{usr} has connected to Discord!".format(usr=client.user)
    # print (str)
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print ("{usr} is connected to the following guild:".format(usr=client.user))
    print ("{name}(id: {id})".format(name=guild.name,id=guild.id))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == 'hi':
        await message.channel.send("Hey")

    if "!google" in message.content.lower():
        i = message.content.find("!google")
        search_str = message.content[i+8:]
        insert_str = "INSERT INTO search_for (search ) VALUES ('{search_str}' );".format(search_str=search_str)
        try:
            cursor.execute(insert_str)
        except Exception as err:
            print("Oops! An exception has occured:", err)
        connection.commit()
        for j in search(search_str, tld="co.in", num=5, stop=5, pause=0):
            await message.channel.send(j)

    if "!recent" in message.content.lower():
        i = message.content.find("!recent")
        search_str = message.content[i+8:]
        cursor.execute("SELECT search from search_for ;")
        rows = cursor.fetchall()
        c = 0
        for row in rows:
            if search_str in row[0]:
                c = 1
                await message.channel.send(row[0])

        if c == 0:
            await message.channel.send("No previous search with {search_str} found".format(search_str=search_str))

client.run(TOKEN)