from helper import *

cogname = "firehousesubs"
class firehousesubs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.firehousesubs_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free medium sub")   
    async def firehousesubs(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.firehousesubs_cd)

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
                    'Host': 'alapp.relevantmobile.com',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Accept': '*/*',
                    'User-Agent': 'Firehouse%20Subs/1.7 CFNetwork/1240.0.4 Darwin/20.5.0',
                    'Accept-Language': 'en-us',
                    'Accept-Encoding': 'gzip, deflate, br',
                }

            data = {
                    'register_type': '1',
                    'zipcode': '90017',
                    'security_question': 'What was your High School Mascot?',
                    'register_device_type': 'iphone',
                    'dob_year': str(random.randint(1950, 1999)),
                    'keychain': ('').join(random.choices(string.ascii_letters.upper() + string.digits.upper(), k=40)), 
                    'marketing_optin': 'true',
                    'last_name': name[1],
                    'dob_month': datetime.datetime.today().strftime('%m').lstrip("0").replace(" 0", " "),
                    'dob_day': datetime.datetime.today().strftime('%d').lstrip("0").replace(" 0", " "),
                    'os': '14.6',
                    'connect_type': '1',
                    'email': random_email,
                    'phone_number': phonenumber,
                    'referral_code': '',
                    'phone_model': 'Unknown Device',
                    'password': password,
                    'security_answer': name[0],
                    'first_name': name[0],
                    'appkey': 't6VVWSrcYaKm1tJE',
                    'favorite_location': '22330'
                }

            try:
                response = await session.post('https://alapp.relevantmobile.com/api/vncr/user/onlineorder/customer_connect', 
                    headers=headers, data=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.firehousesubs_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "saved" in result:
            embed = discord.Embed(title="F̷i̷r̷e̷h̷o̷u̷s̷e̷ S̷u̷b̷s̷", url="https://order.firehousesubs.com/auth/sign-in",
                description=f"Login app or site for a **free medium sub**.\n\n"
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
            await command_error(self, ctx, botmsg, self.bot.firehousesubs_cd, cogname, connector, "BadResponse")
                  
async def setup(bot: commands.Bot):
    await bot.add_cog(firehousesubs(bot))
