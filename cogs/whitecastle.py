from helper import *

cogname = "whitecastle"
class whitecastle(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.whitecastle_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free dessert on a stick")   
    async def whitecastle(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.whitecastle_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = await gen_password()
        phonenumber = f"917{str(random.randint(2, 9))}" + str(random.randint(11, 99)) + str(random.randint(1111, 9999))
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    "User_Agent" : random.choice(self.bot.user_agents),
                    "accept": "application/json",
                    "accept-encoding": "gzip, deflate",
                    "content-type": "application/json; charset=utf-8",
                    "host": "mobileorder.whitecastle.com"
            }

            data = {
                    "UserName": random_email,
                    "FirstName": name[0],
                    "LastName": name[1],
                    "Password": password,
                    "ConfirmPassword": password,
                    "SecurityQuestion": "mother's maiden name?",
                    "SecurityAnswer": names.get_last_name(),
                    "AllowPromotions": True,
                    "Address": str(random.randint(11, 9999)) + f" s {names.get_last_name()} ave",
                    "Address2": "",
                    "City": "los angeles",
                    "State": "CA",
                    "ZipCode": "90040",
                    "PhoneNumber": phonenumber,
                    "MobileNumber": phonenumber,
                    "Company": "",
                    "ReceiveWhiteCastleNews": True,
                    "AllowTextMessages": True,
                    "IsPhoneConsent": True
            }

            try:
                response = await session.post('https://mobileorder.whitecastle.com/MobileV5/orderNow/Data/GetRegisterUserNew', 
                    headers=headers, json=data, ssl=False, timeout=20)

                response = await session.get(f'https://mobileorder.whitecastle.com/MobileV5/orderNow/Data/GetDoesUserExist?emailAddress={random_email}', 
                    headers=headers, ssl=False, timeout=20)

                response = await session.get(f'https://mobileorder.whitecastle.com/MobileV5/orderNow/Data/GetLogin?userName={random_email}&password={password}', 
                    headers=headers, ssl=False, timeout=20)

            except:
                return await command_error(self, ctx, botmsg, self.bot.whitecastle_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if random_email in result:
            embed = discord.Embed(title="W̷h̷i̷t̷e̷ C̷a̷s̷t̷l̷e̷", url="https://order.whitecastle.com/OrderNow/login",
                description=f"Login app for a **free dessert on a stick**.\n\n"
                            "No purchase necessary. Scan in-store to redeem.")
            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            return await command_error(self, ctx, botmsg, self.bot.whitecastle_cd, cogname, connector, "BadResponse")

async def setup(bot: commands.Bot):
    await bot.add_cog(whitecastle(bot))
