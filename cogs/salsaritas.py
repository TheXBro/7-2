from helper import *

cogname = "salsaritas"
class salsaritas(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.salsaritas_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free any entree")   
    async def salsaritas(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.salsaritas_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = await gen_password()
        phonenumber = f"917{str(random.randint(2, 9))}" + str(random.randint(111111, 999999))  
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        captcha_key = await get_captcha_key(ctx, 'https://iframe.punchh.com/customers/sign_up.iframe?slug=salsaritas', '6LfHvSEUAAAAAHuEo7FF0LB8WTgHEtujhS7C6daR')    
        
        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    'User-Agent': random.choice(self.bot.user_agents)
            }

            data = {
                    'user[card_number]':"",
                    'user[email]': random_email,
                    'user[first_name]': name[0],
                    'user[last_name]': name[1],
                    'user[phone]': '',
                    'user[password]': password,
                    'user[password_confirmation]': password,
                    'user[fav_location_id]': '355318',
                    'user[invite_code]': "",
                    'user[birthday(3i)]': datetime.datetime.today().strftime('%d').lstrip("0").replace(" 0", " "),
                    'user[birthday(2i)]': datetime.datetime.today().strftime('%m').lstrip("0").replace(" 0", " "),
                    'user[birthday(1i)]': str(random.randint(1950, 1999)),
                    'user[send_compliance_sms]': [
                                                    '0',
                                                    '1', ], 
                    'g-recaptcha-response': captcha_key 
            }
                
            try:
                response = await session.post('https://iframe.punchh.com/customers.iframe?slug=salsaritas', 
                    headers=headers, data=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.salsaritas_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "successfully" in result:
            embed = discord.Embed(title="S̷a̷l̷s̷a̷r̷i̷t̷a̷s̷", url="https://salsaritas.com/rewards-sign-in/",
                    description=f"Login app or site for a **free entree**.\n\n"
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
            await command_error(self, ctx, botmsg, self.bot.salsaritas_cd, cogname, connector, "BadResponse")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(salsaritas(bot))
