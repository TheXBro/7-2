from helper import *

cogname = "dennys"
class dennys(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.dennys_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free Everyday Value Slam breakfast")   
    async def dennys(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.dennys_cd)

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
                    'Accept': 'application/json, text/plain, */*',
                    'User-Agent': random.choice(self.bot.user_agents) 
            }

            data = {
                    'user': {
                    'email': random_email,
                    'first_name': name[0],
                    'last_name': name[1],
                    'password': password,
                    'phone': phonenumber,
                    'terms_and_conditions': True,
                    'favourite_location_ids': None,
                    'marketing_email_subscription': True,
                    'marketing_pn_subscription': True,
                    'birthday': bday,
                    'send_compliance_sms': False, }
            }

            try:
                response = await session.post('https://nomnom-prod-api.dennys.com/punchhv2/create', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.dennys_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "user_id" in result:
            embed = discord.Embed(title="D̷e̷n̷n̷y̷s̷", url="https://dennys.com/order/rewards",
                description=f"Login app or site for a **free Everyday Value Slam**.\n(2 pancakes, 2 eggs, french toast or biscuit, and bacon or sausage)\n\n"
                            "No purchase necessary. Redeem online or in-store.\n\n"
                            "Use qr-code number at checkout to order online.")
            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            await command_error(self, ctx, botmsg, self.bot.dennys_cd, cogname, connector, "BadResponse")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(dennys(bot))
