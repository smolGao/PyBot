# Import library needed
import discord
import os
# This library allows https request, can be use for webscrapping too
import requests
# Quotes API returned json
import json

# Get quotes from the zenquotes API
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


# Declare client var
# It's required to set intents in the constructor
intents = discord.Intents.default()
# Make sure the attribute is consistent with the discord dev page
intents.message_content = True
client = discord.Client(intents=intents)


# Register events
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


# async allows the object to run in more than one execution
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith("$hello"):
    # await calls the function as async
    await message.channel.send("Hello")
  if message.content.startswith("$inspire"):
    await message.channel.send(get_quote())


client.run(os.getenv('Token'))
