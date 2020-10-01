import os
import discord
from dotenv import load_dotenv
from googlesearch import search
import psycopg2
from os import environ

load_dotenv()
TOKEN = environ['DISCORD_TOKEN']
GUILD = environ['DISCORD_GUILD']

DATABASE_URL = environ['DATABASE_URL']
connection = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = connection.cursor()

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print ("{usr} is connected to the following guild:".format(usr=client.user))
    print ("{name}(id: {id})".format(name=guild.name,id=guild.id))
    insert_str = "CREATE table search_for (search varchar(1000) UNIQUE) ;"

    try:
        cursor.execute(insert_str)
    except Exception as err:
        print("Oops! An exception has occured:", err)
    connection.commit()

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