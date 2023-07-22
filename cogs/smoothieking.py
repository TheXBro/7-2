
from helper import *

cogname = "smoothieking"
class smoothieking(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.smoothieking_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                          description = "$2 reward and free espresso shot")   
    async def smoothieking(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.smoothieking_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = await gen_password()
        phonenumber = f"(917) {str(random.randint(2, 9))}" + str(random.randint(11, 99)) + '-' + str(random.randint(1111, 9999))
        bday = f"{str(random.randint(1950, 1999))}-{datetime.datetime.now().strftime('%m')}-{datetime.datetime.now().strftime('%d')}"   
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)
        
        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    'Host': 'api.thelevelup.com',
                    'X-LevelUp-API-Key': 'BBpmDK5SdS3qxRTi1Q856nMuH4q9bzhpVHyoimF8Te62fEPDxz22XL7tvoaZzRAi',
                    'Accept': 'application/json',
                    'User-Agent': 'Build/4.7.1, LevelUpSDK/14.0.1',
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
                    'api_key': 'BBpmDK5SdS3qxRTi1Q856nMuH4q9bzhpVHyoimF8Te62fEPDxz22XL7tvoaZzRAi',
            }

            try:
                response = await session.post('https://api.thelevelup.com/v14/users', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.smoothieking_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "terms_accepted_at" in result:
            embed = discord.Embed(title="S̷m̷o̷o̷t̷h̷i̷e̷ K̷i̷n̷g̷", url="https://smoothieking.com",
                description=f"Login app for a **free $2 reward** and **free espresso shot**.\n\n"
                            "Redeem online only.")
            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            await command_error(self, ctx, botmsg, self.bot.smoothieking_cd, cogname, connector, "BadResponse")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(smoothieking(bot))
