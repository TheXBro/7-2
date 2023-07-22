from helper import *

cogname = "deltaco"
class deltaco(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.deltaco_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free shake, 2 del taco")   
    async def deltaco(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.deltaco_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = await gen_password()
        print(password)
        phonenumber = f"(91{str(random.randint(2, 9))})" + str(random.randint(222, 999)) + "-" + str(random.randint(1111, 9999))         
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)
        
        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    'User-Agent': random.choice(self.bot.user_agents),
                    'Accept': "application/json, application/vnd.stellar-v1+json",
                    'Accept-Language': "en-US,en;q=0.5",
                    'Accept-Encoding': "gzip, deflate, br",
                    'Content-Type': "application/x-www-form-urlencoded",
                }

            data = "client_id=504cfc0e4d3001b04209a08c5be699a8977959b3bcc621b8e55eed8a8c323d6c&client_secret=f3a191363f052644f33b2e05d341f87e55346383b05724e3fddbbcf9ea41f578&email=" + random_email + "&password=" + password +"&password_confirmation=" + password + "&first_name=" + name[0] + "&last_name=" + name[1] + "&referral_code=&favorite_location=730&mobile_phone=" + phonenumber + "&receive_mail_offers=false&receive_sms_offers=false&birthdate=" + str(random.randint(1950, 1999)) + "-" + datetime.datetime.now().strftime('%m') + "-" + datetime.datetime.now().strftime('%d') + ""

            try:
                response = await session.post('https://cust1184.cheetahedp.com/api/sign_up', 
                    headers=headers, data=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.deltaco_cd, cogname, connector, "RequestTimeout")

            result = await response.text()
            print(result)

        if "true" in result:
            embed = discord.Embed(title="Del Taco", url="https://deltaco.com/rewards/sign-in",
                description=f"Verify email for a **free regular shake** (no purchase necessary)\n"
                            "and **2 free Del Tacos** (any purchase required).\n\n"
                            "Login app or site. Redeem online or in-store.")    

            if "yopmail" in random_email:
                embed.add_field(name=f"email", value=f"[{random_email}](https://yopmail.com/en/?login={random_email})", inline=False)
            else:
                embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            return await command_error(self, ctx, botmsg, self.bot.deltaco_cd, cogname, connector, "BadResponse")

async def setup(bot: commands.Bot):
    await bot.add_cog(deltaco(bot))
