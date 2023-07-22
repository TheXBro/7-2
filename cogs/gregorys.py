
from helper import *

cogname = "gregorys"
class gregorys(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.gregorys_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free any drink")   
    async def gregorys(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.gregorys_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = await gen_password()
        phonenumber = f"917{str(random.randint(2, 9))}" + str(random.randint(111111, 999999))  
        bday = f"{str(random.randint(1950, 1999))}-{datetime.datetime.now().strftime('%m')}-{datetime.datetime.now().strftime('%d')}"      
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    'Host': 'api.thelevelup.com',
                    'X-LevelUp-API-Key': 'd0620c81eb57911f783a8545334d61d9ad8a73f56d259f3e9cac7bab8538963d',
                    'Accept': 'application/json',
                    'User-Agent': 'Build/1.5.0, LevelUpSDK/12.0.2',
                    'Accept-Language': 'en-us',
            }

            data = {
                    'user': {
                        'last_name': name[1],
                        'custom_gender': '',
                        'device_identifier': '035A754E-F4FE-42CC-945F-' + ''.join((random.choice(string.ascii_letters.upper()) for i in range(12))),
                        'gender': '',
                        'first_name': name[0],
                        'password': password,
                        'phone': phonenumber,
                        'email': random_email,
                        'terms_accepted': True,
                    },
                    'api_key': 'd0620c81eb57911f783a8545334d61d9ad8a73f56d259f3e9cac7bab8538963d'
            }

            try:
                response = await session.post('https://api.thelevelup.com/v14/users', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.gregorys_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if random_email in result:
            embed = discord.Embed(title="G̷r̷e̷g̷o̷r̷y̷s̷ C̷o̷f̷f̷e̷e̷", url="https://www.gregoryscoffee.com",
                description=f"Login app or site for any **free drink**. (Discount up to $6.50)\n\n" #edit
                            "No purchase necessary. Redeem online or in-store.")
            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            await command_error(self, ctx, botmsg, self.bot.gregorys_cd, cogname, connector, "BadResponse")
               
async def setup(bot: commands.Bot):
    await bot.add_cog(gregorys(bot))
