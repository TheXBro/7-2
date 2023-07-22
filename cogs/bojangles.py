from helper import *

cogname = "bojangles"
class bojangles(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.bojangles_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free 2pc leg & thigh meal and drink")   
    async def bojangles(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.bojangles_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = await gen_password("exception")
        phonenumber = f"917{str(random.randint(2, 9))}" + str(random.randint(111111, 999999)) 
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)
        
        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                        'accept':'application/json, text/plain, */*',
                        'accept-encoding':'gzip',
                        'client_id':'XMzXxrjALeejfUD2Komc',
                        'client_type':'android',
                        'content-type':'application/json',
                        'host':'offers-prd--bojangles-dev.netlify.app',
                        'path':'members/create',
                        'user-agent': random.choice(self.bot.user_agents),
                        'version':'2'
            }
                        
            data = {
                    "email": random_email,
                    "first_name": name[0],
                    "last_name": name[1],
                    "password": password,
                    "phone": phonenumber,
                    "zip": random_address.real_random_address()['postalCode'],
                    "opt_in": True,
                    "optin_sms": True,
                    "firebase_push_notification_token": "fgpgh0TPTIGWJW-ihSIzU1:APA91bHx2vwPmnIztd-4pnSmd7uUIrOkLBkT8CyLhj1zEm72VA1afCG-NFAoqcLlcXTvU5Oz1t1XoXWm0fLE28iAt8hel442Mlsj8cOV3PD4iJ-qGJwTRI-dd-CHqFY48gMFpyg5j38d"
            }
            
            try:
                response = await session.post('https://offers-prd--bojangles-dev.netlify.app/api', 
                    headers=headers, json=data, ssl=False, timeout=20)                
            except:
                return await command_error(self, ctx, botmsg, self.bot.bojangles_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "access" in result:
            embed = discord.Embed(title="B̷o̷j̷a̷n̷g̷l̷e̷s̷", url="https://www.bojangles.com",
                    description=f"Login app for a **free 2pc leg & thigh + choice of 2 sides** and **free regular drink**.\n\n"
                                "No purchase necessary. Redeem online only.")
            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            return await command_error(self, ctx, botmsg, self.bot.bojangles_cd, cogname, connector, "BadResponse")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(bojangles(bot))
