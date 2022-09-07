import json
import requests
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents,command_prefix='#')

#open("response.json",'w').write(req.text)

def indent(req):
    print(json.dumps(req, indent=4))
    
def formatChannel(req,i):

    channel = req.json()['hits']['hits'][i]
    infos = channel['_source']

    return ('--------[ {} ]--------'.format(i)+'\n'
        +'Langue : '+infos['code']+'\n'
        +'Location : '+infos['subtitle']+'\n'
        +'Titre : '+infos['title']+'\n'
        +'Lien : '+infos['url']+'\n')

@bot.event
async def on_ready():
    print("Bot Ok !")

@bot.command(name="replyChoice")
async def choice(message):
    print(message)

@bot.command()
async def search(ctx, *args):

    passphrase = ""

    req = requests.get("http://radio.garden/api/search?q={}".format(args[0]))
    n= len(req.json()['hits']['hits'])

    if(n>0):
        for i in range(n):
            passphrase+=formatChannel(req,i)

        await ctx.send(passphrase+"\nSelect the number of your choice !")
        
        msg = await bot.wait_for("message",check=choice, timeout=60.0)

        req.json()['hits']['hits'][int(msg.content)]['_source']['title']

    else:
        ctx.send("Aucune chaine a ce nom n'existe. Essayez en une autre")
    

bot.run("")
