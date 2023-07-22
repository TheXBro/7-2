from helper import *

cogname = "capizzakitchen"
class capizzakitchen(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.capizzakitchen_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free small plate + $5 reward")   
    async def capizzakitchen(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.capizzakitchen_cd)

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
                        'User-Agent': random.choice(self.bot.user_agents),
                        'Accept': '*/*',
                        'Content-Type': 'application/json'}

            data = {"authentication": "anonymous",
                        "merchantId": 52,
                        "cardTemplateCode": 1,
                        "activationStoreCode": "pxweb",
                        "enforceUniqueFields": ["mobilePhone",
                                                "email"],
                        "setUserFields": {"style": "typed",
                                        "optIn": True,
                                        "email": [random_email],
                                        "password": [password],
                                        "firstName": [name[0]],
                                        "lastName": [name[1]],
                                        "dateOfBirth": [f"{str(random.randint(1950, 1999)) }-{datetime.datetime.today().strftime('%m')}-{datetime.datetime.today().strftime('%d')}"],
                                        "mobilePhone": [phonenumber],
                                        "username": [random_email]},
                        "setAccountFields": {"style": "typed",
                                            "favoriteStore": [{"code": "155"}]}}

            try:
                response = await session.post('https://api.cpk.com/api/v1.0/users/create', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.capizzakitchen_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "Success" in result:
            embed = discord.Embed(title="C̷a̷l̷i̷f̷o̷r̷n̷i̷a̷ P̷i̷z̷z̷a̷ K̷i̷t̷c̷h̷e̷n̷", url="https://order.capizzakitchen.com/auth/sign-in",
                    description=f"Login app or site for a **free small plate** and **free $5 reward**.\n\n" #edit
                                "No purchase necessary. Redeem online or in-store.\n\n"
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
            return await command_error(self, ctx, botmsg, self.bot.capizzakitchen_cd, cogname, connector, "BadResponse")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(capizzakitchen(bot))
