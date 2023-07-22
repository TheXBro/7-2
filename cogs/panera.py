
from helper import *

cogname = "panera"
class panera(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.panera_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free pastry, sweet treat")   
    async def panera(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.panera_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx, "gmail.com")
        password = await gen_password()
        phonenumber = f"917{str(random.randint(2, 9))}" + str(random.randint(111111, 999999)) 
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    "cookie": "userloc=LOSANGELES%2CCA",
                    "Host": "services-mob.panerabread.com",
                    "Accept": "*/*",
                    "appVersion": "4.66.0",
                    "api_token": "bcf0be75-0de6-4af0-be05-13d7470a85f2",
                    "Accept-Language": "en-us",
                    "User-Agent": "Panera/4.66.0 (iPhone; iOS 15.3; Scale/3.00)",
                    "Content-Type": "application/json"
            }

            data = {
                    "password": password,
                    "emailAddress": random_email,
                    "phoneNumber": phonenumber,
                    "username": phonenumber,
                    "lastName": name[1],
                    "firstName": name[0],
                    "opt": "true",
                    "birthDate": {
                        "birthMonth": datetime.datetime.now().strftime('%m'),
                        "birthDay": datetime.datetime.now().strftime('%d')
                } 
            }

            try:
                response = await session.post('https://services-mob.panerabread.com/register', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.panera_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "customerId" in result:
            embed = discord.Embed(title="P̷a̷n̷e̷r̷a̷", url="https://www.panerabread.com/en-us/home.html",
                description=f"Login app or site for any **free pastry or treat**.\n\n"
                            "Any purchase required. Redeem online or in-store.")
            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            await command_error(self, ctx, botmsg, self.bot.panera_cd, cogname, connector, "BadResponse")
              
async def setup(bot: commands.Bot):
    await bot.add_cog(panera(bot))
