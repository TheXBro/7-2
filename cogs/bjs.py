from helper import *

cogname = "bjs"
class bjs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.bjs_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free Pizookie dessert")   
    async def bjs(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.bjs_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = await gen_password()
        phonenumber = f"917{str(random.randint(2, 9))}" + str(random.randint(111111, 999999))    
        bday = datetime.datetime.now().strftime('%m') + "/" + datetime.datetime.now().strftime('%d') + "/" + str(random.randint(1950, 1999)) 
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                "User-Agent": random.choice(self.bot.user_agents),
                "Accept": "*/*",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
            }

            data = {
                "addressLine1": str(random.randint(111, 999)) + " s main st",
                "addressLine2": "",
                "addressCity": "los angeles", 
                "addressState": "CA",
                "birthDate": bday,
                "email": random_email,
                "firstName": name[0],
                "hasAgreedToRegistrationTerms": True,
                "lastName": name[1],
                "loyaltyId": "",
                "optedInToSMSNotifications": True,
                "password": password,
                "passwordConfirmation": password,
                "phoneNumber": phonenumber,
                "preferredLocationSiteId": "490",
                "zipCode": random_address.real_random_address()['postalCode'],
            }

            try:
                response = await session.post('https://www.bjsrestaurants.com/api/register-loyalty-account', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.bjs_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if random_email in result:
            embed = discord.Embed(title="B̷J̷s̷", url="https://www.bjsrestaurants.com/account/login",
                description=f"Login app or site for a **free Pizookie dessert**.\n\n"
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
            return await command_error(self, ctx, botmsg, self.bot.bjs_cd, cogname, connector, "BadResponse")

async def setup(bot: commands.Bot):
    await bot.add_cog(bjs(bot))
