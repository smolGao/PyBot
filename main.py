# Import library needed
import discord
import os

# This library allows https request, can be use for webscrapping too
import requests

# Quotes API returned json
import json
import random

# Use replit database
from replit import db

# Declare client var
# It's required to set intents in the constructor
intents = discord.Intents.default()

# Make sure the attribute is consistent with the discord dev page
intents.message_content = True
client = discord.Client(intents=intents)

# A list of trigger words
sad_phrases = [
  "sad", "depressed", "unhappy", "angry", "miserable", "depressing",
  "unfortunate"
]

basic_encouragments = [
  "Tomorrow will be better", "Time will elapse", "Sunny day coming"
]


def update_db(val):
  if "encouragements" in db.keys():
    entries = db["encouragements"]
    entries.append(val)
    db["encouragements"] = entries
  else:
    db["encouragements"] = [val]


def delete_entry(index):
  entries = db["encouragements"]
  if index < len(entries):
    print(type(entries))
    del entries[index]
    db["encouragments"] = entries
    return "Delete Sucessfulyy"
  return "Error: IndexOutOfBound"


def show_db():
  res = basic_encouragments
  if "encouragements" in db.keys():
    # Without .value, the list wil be ObservedList and can't be concatenate
    return res + db["encouragements"].value
  return res


# Get quotes from the zenquotes API
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote


# Register events
@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))


# async allows the object to run in more than one execution
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  if msg.startswith("$inspire"):
    await message.channel.send(get_quote())

  options = basic_encouragments

  if "encouragements" in db.keys():
    options = options + db["encouragements"].value

  if any(m in msg for m in sad_phrases):
    await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    new_msg = msg.split("$new ", 1)[1]
    update_db(new_msg)
    await message.channel.send("Added Successfully")

  if msg.startswith("$del"):
    res = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del ", 1)[1])
      await message.channel.send(delete_entry(index))
      res = db["encouragements"]
    await message.channel.send(res.value)

  if msg == "$list":
    await message.channel.send(show_db())


client.run(os.getenv('Token'))
