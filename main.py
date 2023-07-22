import os, time, asyncio, datetime, aiosqlite
import discord
from discord.ext import commands
from discord import app_commands
from config import *
from helper import *
import nest_asyncio

nest_asyncio.apply()


connector = ProxyConnector.from_url(proxies())
class client(commands.Bot):
    def __init__(self):
        super().__init__(
            connector = connector,
            command_prefix = "/",
            intents = discord.Intents.all(),
            application_id = application_id,
            timeout= None)

    async def setup_hook(self):
        list = os.listdir("./cogs")
        bot.modules = len(list)
        
        for filename in list:
           if filename.endswith(".py"):
              await bot.load_extension(f"cogs.{filename[:-3]}")
        
           
    async def on_ready(self):
        print(f"{bot.user.name} is ready.")   
      
        #print(f"Serving free food in {len(self.guilds)} servers:")
        #guilds = list(self.guilds)
        #for guild in self.guilds:
        #    print(f"{guild.name} | Members: {str(guild.member_count)} | Owner: {guild.owner}")
        
    
    async def close(self):
        await super().close()
    
    async def on_command_error(self, ctx, error):
        await ctx.send(error)

bot = client()

bot.remove_command("help")


bot.cooldowntime = 0
bot.command_cooldown_secs = command_cooldown
bot.global_cooldown_secs = global_cooldown

bot.global_cd = []

bot.user_agents = [ #add few more to list
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/102.0.5005.67 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/102.0.5005.87 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/102.0.5005.87 Mobile/15E148 Safari/604.1',
'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/10 Mobile/15E148 Safari/605.1.15 GAYL/2.0.9b1',
'Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/101.0 Mobile/15E148 Safari/605.1.15',
]


async def main():
    bot.db = await aiosqlite.connect("database.db")
    
    await bot.db.execute('''CREATE TABLE IF NOT EXISTS users(
                                        user_id int ,
                                        email text
                                        )''')  #PRIMARY KEY (user_id)

    await bot.db.execute('''CREATE TABLE IF NOT EXISTS accounts(
                                        date text ,
                                        guild_id int ,    
                                        user_id int ,
                                        msg_id int ,
                                        command text,
                                        email text ,
                                        password text 
                                        )''')

    await bot.db.execute('''CREATE TABLE IF NOT EXISTS cooldowns(
                                        guild_id int ,
                                        user_id int ,
                                        global int ,
                                        arbys int ,
                                        aw int ,
                                        blueapron int ,
                                        bjs int ,
                                        bojangles int ,
                                        capizzakitchen int ,
                                        captainds int ,
                                        checkers int ,
                                        chilis int ,
                                        deltaco int ,
                                        dennys int ,
                                        einsteinbros int ,
                                        elpolloloco int ,
                                        everyplate int ,
                                        everytable int ,
                                        factor int ,
                                        firehousesubs int ,
                                        freddys int ,
                                        freerest int ,
                                        freshly int ,
                                        goodchop int ,
                                        goodeggs int ,
                                        greenchef int ,
                                        gregorys int ,
                                        halalguys int ,
                                        hellofresh int ,
                                        homechef int ,
                                        hungryroot int ,
                                        imperfectfoods int ,
                                        krispykreme int ,
                                        littlebigburger int ,
                                        mcdonalds int,
                                        nurturelife int ,
                                        ocharleys int,
                                        panera int,
                                        pollocampero int,
                                        qdoba int ,
                                        rallys int ,
                                        redrobin int ,
                                        restaurant int ,
                                        rubios int ,
                                        salsaritas int ,
                                        smoothieking int ,
                                        sonic int ,
                                        steaknshake int ,
                                        sunbasket int ,
                                        tacobell int ,
                                        tgifridays int ,
                                        thrivemarket int ,
                                        tkungfutea int ,
                                        wafflehouse int ,
                                        wendys int ,
                                        whataburger int ,
                                        whitecastle int ,
                                        wienerschnitzel int ,
                                        yoshinoya int ,
                                        PRIMARY KEY (guild_id, user_id)
                                        )''')
    async with bot:
         await bot.start(bot_token)
    
    await bot.db.close()

    
     
asyncio.run(main())        
