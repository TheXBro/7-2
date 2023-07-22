
from helper import *

cogname = "krispykreme"
class krispykreme(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.krispykreme_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free dozen donuts")   
    async def krispykreme(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.krispykreme_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = await gen_password()
        phonenumber = f"917-{str(random.randint(2, 9))}" + str(random.randint(111111, 999999)) 
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {'User-Agent': 'aws-sdk-iOS/2.25.1 iOS/14.0 en_US'}

            data = {
                        "source": "iOS",
                        "password": password,
                        "firstName": name[0],
                        "appVersion": "22.2.0",
                        "phoneNumber": phonenumber,
                        "birthday": datetime.datetime.today().strftime('%m') + "/" + datetime.datetime.today().strftime('%d'),
                        "email": random_email,
                        "zipCode": random_address.real_random_address()['postalCode'],
                        "lastName": name[1] 
            }

            try:
                response = await session.post('https://api.krispykreme.com/auth/createaccount', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.krispykreme_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if ("true" in result) or ("Endpoint request timed out" in result):
            embed = discord.Embed(title="K̷r̷i̷s̷p̷y̷ K̷r̷e̷m̷e̷", url="https://krispykreme.com/account/sign-in",
                description=f"Login app or site for a **free dozen glazed donuts** and a **free donut of choice**.\n\n" #edit
                            "No purchase necessary. Scan in-store to redeem.\n\n"
                            "Allow ~24 hours for offer to appear.")
            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            await command_error(self, ctx, botmsg, self.bot.krispykreme_cd, cogname, connector, "BadResponse")
               
async def setup(bot: commands.Bot):
    await bot.add_cog(krispykreme(bot))
