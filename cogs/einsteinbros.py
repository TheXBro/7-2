from helper import *

cogname = "einsteinbros"
class einsteinbros(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.einsteinbros_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free bagel with spread & coffee")   
    async def einsteinbros(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.einsteinbros_cd)

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
                    'Host': 'api.bagelbrands.com',
                    'Accept': '*/*',
                    'sourceAppVersion': '3.37.0 (2022070101)',
                    'Accept-Language': 'en-US;q=1.0',
                    'x-source-app': 'EBBApp',
                    'sourceAppBrand': 'EBBApp',
                    'User-Agent': 'Ebb_PROD_Env/3.37.0 (com.ebb.ebbapp; build:2022070101; iOS 14.5.0) Alamofire/5.0.0-rc.2',
                    'Ocp-Apim-Subscription-Key': '08d5c53223c844adb470897b1032ff97',
                    'sourceAppPlatform': 'iOS',
                }

            data = {
                    'sourceApp': 'EBBApp',
                    'create': {
                        'credentials': {
                            'password': password,
                            'userName': random_email,
                        },
                        'preferences': {
                            'ebbEmail': True,
                            'cateringEmail': True,
                            'ebbProgram': True,
                        },
                        'personalInfo': {
                            'emailAddress': random_email,
                            'lastName': name[1],
                            'firstName': name[0],
                            'gender': 'PreferNotToAnswer',
                            'address': {
                                'zip': '90040',
                                'city': 'Los Angeles',
                                'state': 'CA',
                            },
                            'memberPhone': phonenumber,
                            'dateOfBirth': bday,
                        },
                    },
                }

            try:
                response = await session.post('https://api.bagelbrands.com/account/v2/create', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.einsteinbros_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "Success" in result:
            embed = discord.Embed(title="E̷i̷n̷s̷t̷e̷i̷n̷ B̷r̷o̷s̷ B̷a̷g̷e̷l̷s̷", url="https://rewards.einsteinbros.com/login",
                description=f"Login app for a **free bagel and spread** and a **free hot or iced coffee**.\n\n"
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
            await command_error(self, ctx, botmsg, self.bot.einsteinbros_cd, cogname, connector, "BadResponse")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(einsteinbros(bot))
