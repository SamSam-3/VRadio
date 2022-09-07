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
    

@bot.event
async def on_ready():
    print("Bot Ok !")

@bot.command(name="replyChoice")
async def choice(message):
    print(message)

@bot.command()
async def search(ctx, *args):

    req = requests.get("http://radio.garden/api/search?q={}".format(args[0]))
    n= len(req.json()['hits']['hits'])
    passphrase = ""

    if(n>0):
        for i in range(n):

            channel = req.json()['hits']['hits'][i]
            infos = channel['_source']

            passphrase+=('--------[ {} ]--------'.format(i)+'\n'
                +'Langue : '+infos['code']+'\n'
                +'Location : '+infos['subtitle']+'\n'
                +'Titre : '+infos['title']+'\n'
                +'Lien : '+infos['url']+'\n')

        await ctx.send(passphrase)

        msg = await bot.wait_for("message",check=choice, timeout=60.0)
        print(msg.content)

    else:
        ctx.send("Aucune chaine a ce nom n'existe. Essayez en une autre")
    

#bot token : MTAxNjY3NDY4MzAzNjM4NTM4Mg.GUAUHC.GM3WdBtMU89Rp7s5Ngosjbp-jeGmaVVtDsYFh4
bot.run("MTAxNjY3NDY4MzAzNjM4NTM4Mg.GUAUHC.GM3WdBtMU89Rp7s5Ngosjbp-jeGmaVVtDsYFh4")
