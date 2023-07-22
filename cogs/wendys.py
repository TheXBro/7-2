from helper import *

cogname = "wendys"
class wendys(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.wendys_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free cheeseburger or 10 piece nuggets")   
    async def wendys(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.wendys_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = await gen_password()
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    'User-Agent': random.choice(self.bot.user_agents),
                    'Accept': 'application/json',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Content-Type': 'application/json',
            }

            params = {
                    'lang': 'en',
                    'cntry': 'US',
                    'sourceCode': 'ORDER.WENDYS',
                    'version': '13.0.2',
            }

            data = {"lang":"en",
                        "cntry":"US",
                        "deviceId":"3cc03e84-0c1b-4c97-a79a-" + ''.join((random.choice(string.ascii_letters.lower()) for i in range(12))),
                        "sourceCode":"ORDER.WENDYS",
                        "version":"13.0.2",
                        "firstName":name[0],
                        "lastName":name[1],
                        "login":random_email,
                        "birthdate":"11011989",
                        "password":password,
                        "terms":True,
                        "optIn":True,
                        "postal": random_address.real_random_address()['postalCode'],
                        "isLoyaltyProfile":True 
                   }

            try:
                response = await session.post('https://customerservices.wendys.com/CustomerServices/rest/createProfile', 
                    headers=headers, json=data, params=params, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.wendys_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "SUCCESS" in result:
            embed = discord.Embed(title="W̷e̷n̷d̷y̷s̷", url="https://order.wendys.com/rewards-home",
                description=f"Login app or site for a **free Dave's single cheeseburger**"
                            "or a **free 10 piece nuggets**.\n\n"
                            "Any purchase required. Redeem online only.")
            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            return await command_error(self, ctx, botmsg, self.bot.wendys_cd, cogname, connector, "BadResponse")
  
async def setup(bot: commands.Bot):
    await bot.add_cog(wendys(bot))
