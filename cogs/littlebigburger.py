from helper import *

cogname = "littlebigburger"
class littlebigburger(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.littlebigburger_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free root beer float")   
    async def littlebigburger(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.littlebigburger_cd)

        await check_roles(ctx, role_id)


        random_email = await check_emails(self, ctx)
        password = await gen_password()
        phonenumber = f"917-{str(random.randint(2, 9))}" + str(random.randint(11, 99)) + '-' + str(random.randint(1111, 9999))
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    "accept": "application/json",
                    "accept-encoding": "gzip",
                    "accept-version": "v3.3",
                    "access-control-allow-origin": "*",
                    "content-type": "application/json",
                    "host": "api-v3.thanx.com",
                    "thanx-app": "55",
                    "thanx-merchant": "littlebigburger",
                    "user-agent:": "Little Big Burger/9.0.7 Android/7.0.1"
            }

            data = {
                    "user": {
                            "email": random_email,
                            "signup_flow": "legacy"
                }
            }

            try:
                response = await session.post('https://api-v3.thanx.com/users', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.littlebigburger_cd, cogname, connector, "RequestTimeout")

            result = await response.json()
            bearer_token = result['access_token']

            headers = {
                    "accept": "application/json",
                    "accept-encoding": "gzip",
                    "accept-version": "v3.3",
                    "access-control-allow-origin": "*",
                    "Authorization": "Bearer " + bearer_token,
                    "content-type": "application/json",
                    "host": "api-v3.thanx.com",
                    "thanx-app": "55",
                    "thanx-merchant": "littlebigburger",
                    "user-agent:": "Little Big Burger/9.0.7 Android/7.0.1"
            }

            data = {
                    "user": {
                        "first_name": name[0],
                        "last_name": name[1],
                        "phone": phonenumber,
                        "has_completed_registration": True,
                        "birth": {
                            "day": int(datetime.datetime.today().strftime('%d').lstrip("0").replace(" 0", " ")),
                            "month": int(datetime.datetime.today().strftime('%m').lstrip("0").replace(" 0", " ")),
                            "year": random.randint(1950, 1999)
                    }
                }
                    
            }

            try:
                response = await session.patch('https://api-v3.thanx.com/users/me', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.littlebigburger_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "complete" in result:
            embed = discord.Embed(title="L̷i̷t̷t̷l̷e̷ B̷i̷g̷ B̷u̷r̷g̷e̷r̷", url="https://order.thanx.com/littlebigburger",
                description=f"Login app for a **free root beer float**.\n\n" #edit
                            "No purchase necessary. Redeem online or in-store")
            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            await command_error(self, ctx, botmsg, self.bot.littlebigburger_cd, cogname, connector, "BadResponse")
               
async def setup(bot: commands.Bot):
    await bot.add_cog(littlebigburger(bot))
