import aiohttp, asyncio, time, names, random, datetime, string
import aiosqlite, aiofiles, random_address
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ui import Button, View
from random_username.generate import generate_username
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector
from typing import Optional
from aiocfscrape import CloudflareScraper
import cloudscraper
from config import *


async def check_name(ctx, name):
        if name is None:
            name = names.get_full_name()
       
        try:
            name = name.split()
                    
        except:
            embed = discord.Embed(description=f"Invalid name. {ctx.author.mention}")
            embed.set_author(name="Oops! Something went wrong.")  
            await ctx.reply(embed=embed)
            return await ctx.error
        
        if (not name[0].isalpha()) or (not name[1].isalpha()) or (not name[1]):
                embed = discord.Embed(description=f"Invalid name. {ctx.author.mention}")
                embed.set_author(name="Oops! Something went wrong.")  
                await ctx.reply(embed=embed)
                return await ctx.error
        
        return name
      


async def gen_password(*exception):
    if exception:
        password = 'Food' + ''.join((random.choice(string.ascii_letters.lower()) for i in range(3))) + ''.join((random.choice(string.digits) for i in range(2))) + "!"
        return password
    
    passes = [
        'Food' + ''.join((random.choice(string.ascii_letters.lower()) for i in range(3))) + ''.join((random.choice(string.digits) for i in range(1))) + "!",
        ''.join((random.choice(string.ascii_letters.lower()) for i in range(3))) + ''.join((random.choice(string.digits) for i in range(1))) + "Food" + "!",
        'food' + ''.join((random.choice(string.ascii_letters.lower()) for i in range(1))) + ''.join((random.choice(string.ascii_letters.lower()) for i in range(2))) + ''.join((random.choice(string.digits) for i in range(1))) + "!",
        ''.join((random.choice(string.ascii_letters.upper()) for i in range(1))) + ''.join((random.choice(string.ascii_letters.lower()) for i in range(2))) + ''.join((random.choice(string.digits) for i in range(1))) + "food" + "!",
    ]
    
    password = random.choice(passes)
    
    return password



async def command_error(self, ctx, botmsg, command_cd, cogname, connector, error):
    bot = self.bot
    print(f"{error}: {cogname}(user_id:{ctx.author.id}, ip: {connector._proxy_host}:{connector._proxy_port})")

    try:
        if ctx.author.id in command_cd:
            command_cd.remove(ctx.author.id) 

        if ctx.author.id in self.bot.global_cd:     
            self.bot.global_cd.remove(ctx.author.id) 
    except:
        pass

    embed = discord.Embed(description=f"Retry command. {ctx.author.mention}")
    embed.set_author(name="Oops! Something went wrong.")  
    await botmsg.edit(embed=embed)
            


async def update_database(self, ctx, name, msg_id, random_email, password):
    async with self.bot.db.cursor() as cursor:
        await cursor.execute("""INSERT OR IGNORE INTO accounts 
                        (date, guild_id, user_id, msg_id, command, email, password) VALUES (?,?,?,?,?,?,?)""", 
                        (datetime.datetime.now().strftime(f"%Y%m%d"),
                        ctx.message.guild.id,
                        ctx.author.id,
                        msg_id,
                        name,
                        random_email,
                        password,
                        ))  

        await cursor.execute(f"UPDATE cooldowns SET global = {time.time()} WHERE guild_id = ? AND user_id = ?", (ctx.message.guild.id, ctx.author.id))   
        await cursor.execute(f"UPDATE cooldowns SET {name} = {time.time()} WHERE guild_id = ? AND user_id = ?", (ctx.message.guild.id, ctx.author.id))   
        await self.bot.db.commit()



async def check_emails(self, ctx, *args): #default - yopmail.com
        try:
            async with self.bot.db.cursor() as cursor:
                await cursor.execute(f"SELECT email FROM users WHERE user_id = {ctx.author.id}") 
                catchall = await cursor.fetchone()
                print(catchall)
                catchall = catchall[0]
                print(catchall)

            random_email = (generate_username()[0] + str(random.randint(11,99)) + '@' + catchall).lower()

        except:
            try:
                random_email = (generate_username()[0] + str(random.randint(11, 99)) + '@' + args[0]).lower()

            except:
                random_email = (generate_username()[0] + str(random.randint(11, 99)) + '@' + 'yopmail.com').lower()
        
        print(random_email)
        return random_email


    
#command cooldown converter
def hms(seconds):
                h = seconds // 3600
                m = seconds % 3600 // 60
                s = seconds % 3600 % 60
                if h ==12:
                    return '`{}` hours.'.format(h)
                if h > 10:
                    return '`{}` hours.'.format(1 + h)
                elif h > 1:
                    return '`{}` hours.'.format(h)
                elif h == 1:
                    return '`{}` minutes.'.format(60 + m)
                elif m == 1:
                    return '`{}` seconds.'.format(60 + s)
                elif m < 1:
                    return '`{}` seconds.'.format(s)
                elif h < 1:
                    return '`{}` minutes.'.format(m)

                

async def check_cooldowns(self, ctx, name, command_cd):
        async with self.bot.db.cursor() as cursor:
            await cursor.execute(f"SELECT {name} FROM cooldowns WHERE guild_id = ? AND user_id = ?", (ctx.message.guild.id, ctx.author.id,))  
            cool_down = await cursor.fetchone()
        
        try:
            time_passed = time.time() - cool_down[0]

        except:
            async with self.bot.db.cursor() as cursor:
                await cursor.execute("INSERT OR IGNORE INTO cooldowns (guild_id, user_id) VALUES (?,?)", (ctx.message.guild.id, ctx.author.id,))  
            await self.bot.db.commit()
            time_passed = 0
        

        if (ctx.author.id in command_cd) and (time_passed < self.bot.command_cooldown_secs):
            embed = discord.Embed(description=f"Try again in {hms(round(self.bot.command_cooldown_secs - time_passed))}")
            embed.set_author(name="Cooldown!")
            await ctx.reply(embed=embed, delete_after=3600)
            await ctx.error

        #if ctx.author.id in command_cd:
        #    command_cd.remove(ctx.author.id) 

        
        async with self.bot.db.cursor() as cursor:
            await cursor.execute("SELECT global FROM cooldowns WHERE guild_id = ? AND user_id = ?", (ctx.message.guild.id, ctx.author.id,))  
            cool_down = await cursor.fetchone()

        try:
            time_passed = time.time() - cool_down[0]
        except:
            pass

        if (ctx.author.id in self.bot.global_cd) and (time_passed < self.bot.global_cooldown_secs):
            cd = round(self.bot.global_cooldown_secs - time_passed)
            global_cooldown_secstime = round(cd/60)
                    
            if (global_cooldown_secstime == 0) or (global_cooldown_secstime == 1):
                embed = discord.Embed(description="Try again in `1` minute.")
                embed.set_author(name="Slowdown!")
                await ctx.reply(embed=embed, delete_after=300)
                #await ctx.reply.errors
                    
            else:
                embed = discord.Embed(description= f"Try again in `{global_cooldown_secstime}` minutes.")
                embed.set_author(name="Slowdown!")
                await ctx.reply(embed=embed, delete_after=300)
            await ctx.error

        #if ctx.author.id in self.bot.global_cd:
        #        self.bot.global_cd.remove(ctx.author.id)

        if ctx.author.id in command_cd:
            pass
        else:
            command_cd.append(ctx.author.id)

        if ctx.author.id in self.bot.global_cd:
            pass
        else:    
            self.bot.global_cd.append(ctx.author.id)



async def check_roles(ctx, role_id):
    role = discord.utils.find(lambda r: r.id == role_id, ctx.message.guild.roles)
    role1 = discord.utils.find(lambda r: r.id == role_id, ctx.message.guild.roles)
    
    #freerole = discord.utils.find(lambda r: r.name == 'hungry', ctx.message.guild.roles)

    #if freerole in ctx.author.roles:
    #    embed = discord.Embed(description=f"Missing permissions.\n\nAvailable free commands:\n"
    #                    "**freerest** - restaurant.com random credit\n"
    #                    "**kungfutea** - free $2 reward\n\n"
    #                    "Join support server to purchase full access.\nhttps://discord.gg/QjYc4NujaH")

    #    await ctx.reply(embed=embed)
        #await ctx.reply.errors
    #    return

    #lse:
    #    pass

    if (role in ctx.author.roles) or (role1 in ctx.author.roles):
        pass
    else:
        embed = discord.Embed(description=f"Missing <@&{str(role_id)}> role.")
        embed.set_author(name="Oops!")
        #    await botmsg.edit(embed=newembed)
        #embed = discord.Embed(description="Missing <@&1014287585146839231>\n\nAccess to <@1014374648546336829> beta requirements:\n• Join our <#1014296812313653310> and\n• maintain 5 verified server invites or a server boost.\n\nTry:\n `/food` to view all 35+ available commands\n`/invites` in <#1014287290694123520>\n\n<#1014295787225751583> and ping <@&1014287518864261140> when you meet requirements for role.")
           #"https://discord.gg/QjYc4NujaH")
        #embed.set_thumbnail(url=url)
        await ctx.reply(embed=embed)
        await ctx.reply.error



# DM buttons    
class PersistentView(View):
    def __init__(self):
        super().__init__(timeout=None)

        #children = self.children
        #self.clear_items()
        self.add_item(discord.ui.Button(label= "Support", style= discord.ButtonStyle.url, 
            url="https://discord.gg/freefood"))
        #for item in children:
        #    self.add_item(item)              
    

    @discord.ui.button(label = "Copypaste", style= discord.ButtonStyle.secondary, custom_id='Copypaste' )
    async def copypaste(self, interaction: discord.Interaction,  button: Button):
        try:
            await interaction.response.defer()
        except:
            pass 

        db = await aiosqlite.connect("database.db")

        async with db.cursor() as cursor:
            await cursor.execute(f"SELECT email FROM accounts WHERE msg_id = ?", (interaction.message.id,))  
            email = await cursor.fetchone()
            email = email[0]

            await cursor.execute(f"SELECT password FROM accounts WHERE msg_id = ?", (interaction.message.id,))  
            password = await cursor.fetchone()
            password = password[0]

        
        try:
            if password == None:
                await interaction.user.send(email)#, delete_after=86400) 
            else:
                await interaction.user.send(email)#, delete_after=86400) 
                await interaction.user.send(password)#, delete_after=86400) 
        except: 
            pass
        

    #@discord.ui.button(label = "Del", style= discord.ButtonStyle.red, custom_id='Delete' )
    #async def delete(self, interaction: discord.Interaction,  button: Button):
    #    db = await aiosqlite.connect("Foodbot\\foodbot.db")

    #    async with db.cursor() as cursor:
    #        await cursor.execute(f"SELECT user_id FROM accounts WHERE msg_id = ?", (interaction.message.id,))  
    #        user_id = await cursor.fetchone()
    #        user_id = user_id[0]  

    #    async with db.cursor() as cursor:
    #        await cursor.execute(f"SELECT user_id FROM accounts WHERE msg_id = ?", (interaction.message.id,))  
    #        user_id = await cursor.fetchone()
    #        user_id = user_id[0] 

    #    user = interaction.client.get_user(user_id) #user_id
    #    channel = await user.create_dm()
    #    message = channel.get_partial_message(interaction.message.id) #msg_id
    #    await message.delete()



async def get_captcha_key(ctx, url, website_key):
    async with aiohttp.ClientSession() as session: #connector=connector
            data = {
                    'clientKey': 'c2931e2c8dace11d49487ad2685cb374',
                    'task': {
                        'type': 'RecaptchaV2TaskProxyless',
                        'websiteURL': url,
                        'websiteKey': website_key,
                    },
                    'softId': 0,
                    'languagePool': 'en',
                        }

            headers = {
                    'Accept': 'application/json',
                            }
                
            response = await session.post('https://api.anti-captcha.com/createTask', json=data, headers=headers, ssl=False)
            resu = await response.json()
            result = resu["taskId"]

            data =                {
                    'clientKey': 'c2931e2c8dace11d49487ad2685cb374',
                    'taskId': result
                }
                
            timeout = 180
            timeout_start = time.time()
            #print(f"Solving captcha...")
            while time.time() < timeout_start + timeout:
                response = await session.post('https://api.anti-captcha.com/getTaskResult', json=data, headers=headers, ssl=False)
                resu = await response.json()
                if resu["status"] == 'processing':
                    #print(resu)
                    await asyncio.sleep(5)
                else:
                    captcha_key = resu['solution']['gRecaptchaResponse']
                    return captcha_key
            
            while True:
                await ctx.error
