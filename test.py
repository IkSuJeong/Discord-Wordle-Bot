import discord
import re
import json
import numpy as np
from discord.ext import commands
#from discord.ext.commands import Bot

black_square = '⬛'

green_square = '🟩'
orange_square = '🟧'

yellow_square = '🟨'
blue_square = '🟦'



#client = discord.Client()
bot = commands.Bot(command_prefix='$')

#changed from on_ready to on_connect
@bot.event
async def on_ready():
    print('Bot logged in as ' + str(bot.user))

@bot.event
async def on_message(message):
    if re.match(r'Wordle [0-9]{3} [1-6X]/6', message.content):
        updateStorage(message)  
    await bot.process_commands(message)

def findLineAccuracy(line):
    yellows = len(re.findall(yellow_square, line))
    if yellows == 0:
        yellows = len(re.findall(blue_square, line))
    greens = len(re.findall(green_square, line))
    if greens == 0:
        greens = len(re.findall(orange_square, line))
    return (yellows, greens)
    
def updateStorage(message):
    lines = message.content
    id = str(message.author.id)

    with open('storage.json', mode = 'r') as file:
        storage = json.load(file)
    try: 
        person = storage[id]
    except:
        with open('template.json', mode = 'r') as file:
            person = json.load(file)['id']
    lines = lines.split('\n')
    line_one = re.findall(r'[1-6X]/6', lines[0])[0]
    try:
        person['tries'].append((int)(re.sub('/6', '', line_one)))
    except:
        person['tries'].append(np.NaN)

    for idx in range(1, 7):
        try:
            line = lines[idx + 1]
            (yellow, green) = findLineAccuracy(line)
            black = 5 - yellow - green
        except:
            yellow = green = black = np.NaN
        person[f'line_{idx}']['Yellow'].append(yellow)
        person[f'line_{idx}']['Green'].append(green)
        person[f'line_{idx}']['Black'].append(black)

    storage[id] = person
    with open('storage.json', mode = 'w', encoding = 'utf-8') as f:
        json.dump(storage, f, ensure_ascii = False, indent = 4)


@bot.command()
async def downloadWordles(ctx):
    channel = bot.get_channel(730839966472601622)
    messages = await ctx.channel.history(limit=200).flatten()
    for message in messages:
        if re.match(r'Wordle [0-9]{3} [1-6]/6', message.content):
            updateStorage(message)  
    

@bot.command()
async def ping(ctx):
    print('pong')
    await ctx.send('pong')

'''
Will overwrite the usual print()
@client.command()
async def print(arg):
    channel = client.get_channel(940147277102710817)
    await channel.send(arg)
'''
        
token = 'TOKEN-HERE'

bot.run(token)
