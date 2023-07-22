from helper import *

cogname = "chilis"
class chilis(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.chilis_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free chips & salsa, non-alcoholic drink")   
    async def chilis(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.chilis_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = await gen_password()
        phonenumber = f"917{str(random.randint(2, 9))}" + str(random.randint(111111, 999999)) 
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    'Host': "gsapi.brinker.com",
                    'Content-Type': "application/x-www-form-urlencoded",
                    'User-Agent': "Chili's/1.0 CFNetwork/1220.1 Darwin/20.5.0",
                    'Accept': "*/*",
                    'Accept-Language': "en-us",
                    'Authorization': "Basic Y2hpbGlzX2lvczphb0FzbjR4S29mQk9KWGxpQjZEanFLTWRHREE0WTAzclQwSFlmQ3c4",
                    'Accept-Encoding': "gzip, deflate, br"
            }

            data = "grant_type=client_credentials"

            try:
                response = await session.post('https://gsapi.brinker.com/v1.0.0/oauth/token', 
                    headers=headers, data=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.chilis_cd, cogname, connector, "RequestTimeout")

            result = await response.json()
            bearer_token = "Bearer " + result['access_token']
            
            headers = {
                    'Host': "gsapi.brinker.com",
                    'Content-Type': "application/json",
                    'User-Agent': "Chili's/1.0 CFNetwork/1220.1 Darwin/20.5.0",
                    'Accept': "*/*",
                    'Authorization': bearer_token
            }

            data = { "storeGUID":"",
                        "dob":f"{str(random.randint(1950, 1999))}-10-01",
                        "source":"chilisapp",
                        "over18":True,
                        "terminalID":"",
                        "lastName": name[1],
                        "mobileOptIn":True,
                        "email":random_email,
                        "address": {"zip":random_address.real_random_address()['postalCode'],
                                    "country":"US"},
                        "userState":0,
                        "channelType":2,
                        "phoneNumber":phonenumber,
                        "channelID":"",
                        "password":password,
                        "storeCode":"0010051139",
                        "firstName": name[0],
                        "enrollmentChannel":None,
                        "enrollmentDate":""
            }
                                        
            try:
                response = await session.post('https://gsapi.brinker.com/v1.0.0/api/join/mca', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.chilis_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "memberID" in result:
            embed = discord.Embed(title="C̷h̷i̷l̷i̷s̷", url="https://chilis.com/",
                description=f"Login for **free chips & salsa** or a **free non-alcoholic drink**.\n\n"
                            "Purchase required. Redeem online or in-store.")
            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)
        else:
            return await command_error(self, ctx, botmsg, self.bot.chilis_cd, cogname, connector, "BadResponse")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(chilis(bot))
