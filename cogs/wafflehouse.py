from helper import *

cogname = "wafflehouse"
class wafflehouse(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.wafflehouse_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free 2 topping hashbrown")   
    async def wafflehouse(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.wafflehouse_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx, "e3b.org")
        password = None
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
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
            }

            cookies = {
                    'PHPSESSID': 'tdg246i71fu859itaf78t1jv8h',
            }

            data = {
                    'fn': name[0],
                    'ln': name[1],
                    'em': random_email,
                    'emcon': random_email,
                    'bmon': '11',
                    'bday': '1',
                    'zip': random_address.real_random_address()['postalCode'],
                    'theaction': 'regulars-club-two',
            }

            try:
                response = await session.post('https://www.wafflehouse.com/doprocess', 
                    headers=headers, data=data, cookies=cookies, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.wafflehouse_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "1" in result:
            embed = discord.Embed(title="W̷a̷f̷f̷l̷e̷h̷o̷u̷s̷e̷", url="https://www.wafflehouse.com/nutrition/hashbrowns/",
                description=f"Check email for a **free 2 topping hashbrown**.\n\n"
                            "No purchase necessary. Scan in-store to redeem.")

            if "e3b" in random_email:
                email = random_email.split("@")
                embed.add_field(name=f"email", value=f"[{email[0]}@yopmail.com](https://yopmail.com/en/?login={email[0]}@yopmail.com)", inline=False)
            else:
                embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)

            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            return await command_error(self, ctx, botmsg, self.bot.wafflehouse_cd, cogname, connector, "BadResponse")

async def setup(bot: commands.Bot):
    await bot.add_cog(wafflehouse(bot))
