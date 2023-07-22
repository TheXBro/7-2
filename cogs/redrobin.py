
from helper import *

cogname = "redrobin"
class redrobin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.redrobin_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                          description = "Free custom burger")   
    async def redrobin(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.redrobin_cd)

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
                            'marketing_pn_subscription': False,
                            'anniversary': None,
                            'birthday': f"01/{datetime.datetime.now().strftime('%m')}/{str(random.randint(1950, 1999))}",
                            'send_compliance_sms': None,
                            'profile_field_answers': {
                                'upf3': 'true',
                                'upf4': 'false',
                                'upf5': 'opted_in',
                            },
                        },
                        'ignore': None,
            }

            try:
                response = await session.post('https://nomnom-prod-api.redrobin.com/punchhv2/create', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.redrobin_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if random_email in result:
            embed = discord.Embed(title="R̷e̷d̷ R̷o̷b̷i̷n̷", url="https://www.redrobin.com/account/login",
                description=f"Login app or site for a **free custom burger**.\n\n" #edit
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
            await command_error(self, ctx, botmsg, self.bot.redrobin_cd, cogname, connector, "BadResponse")
            print(result)
               
async def setup(bot: commands.Bot):
    await bot.add_cog(redrobin(bot))
