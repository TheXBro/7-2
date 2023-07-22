from helper import *

cogname = "pollocampero"
class pollocampero(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.pollocampero_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free $10 reward")   
    async def pollocampero(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.pollocampero_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = await gen_password()
        phonenumber = f"917{str(random.randint(2, 9))}" + str(random.randint(111111, 999999))  
        bday = f"{str(random.randint(1950, 1999))}-{datetime.datetime.now().strftime('%m')}-{datetime.datetime.now().strftime('%d')}" 
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        captcha_key = await get_captcha_key(ctx, 'https://iframe.punchh.com/customers/sign_up.iframe?slug=pollocampero', '6LfHvSEUAAAAAHuEo7FF0LB8WTgHEtujhS7C6daR')    
        
        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    'User-Agent': random.choice(self.bot.user_agents)
            }

            data = {
                    'user[email]': random_email,
                    'user[first_name]': name[0],
                    'user[last_name]': name[1],
                    'user[phone]': '',
                    'user[password]': password,
                    'user[password_confirmation]': password,
                    'user[invite_code]': "",
                    'user[birthday(3i)]': datetime.datetime.today().strftime('%d').lstrip("0").replace(" 0", " "),
                    'user[birthday(2i)]': datetime.datetime.today().strftime('%m').lstrip("0").replace(" 0", " "),
                    'user[birthday(1i)]': str(random.randint(1950, 1999)),
                    'user[zip_code]': random_address.real_random_address()['postalCode'],
                    'user[fav_location_id]': '343015',
                    'user[send_compliance_sms]': '0',
                    'g-recaptcha-response': captcha_key 
            }

            try:
                response = await session.post('https://iframe.punchh.com/customers.iframe?slug=pollocampero', 
                    headers=headers, data=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.pollocampero_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "successfully" in result:
            embed = discord.Embed(title="P̷o̷l̷l̷o̷ C̷a̷m̷p̷e̷r̷o̷", url="https://us.campero.com",
                description=f"Login app or site for a **free $10 reward**.\n\n"
                            # "$10 reward redeems for multiple free items.\n"
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
            await command_error(self, ctx, botmsg, self.bot.pollocampero_cd, cogname, connector , "BadResponse")
               
async def setup(bot: commands.Bot):
    await bot.add_cog(pollocampero(bot))