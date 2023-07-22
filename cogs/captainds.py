from helper import *

cogname = "captainds"
class captainds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.captainds_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free fish and fries")   
    async def captainds(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.captainds_cd)

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
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Origin': 'https://www.captainds.com',
                    'DNT': '1',
                    'Upgrade-Insecure-Requests': '1',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-site',
                    'Sec-Fetch-User': '?1',
                    'Pragma': 'no-cache',
                    'Cache-Control': 'no-cache',
            }

            data = {
                    'crvs': 'hj8DUzs3ID-3PTnoCEYQBZnP-ywiXCvSIopgDNLjkjJeGbwH2m4cxIDJ39cFaXhH2WquANV18uQgqtxlK2K4sJafi7Z0WnDABMIPSsQALmH6o1vegEgQPlgv9vf8nZix-TK9MXgcrHk5OBUX_tCVk2y4M65aariDsX0bun-O9-j44WpVh40hUERh7YAnY1kt',
                    'ABC': '',
                    'XYZ': '',
                    'AtZ': '',
                    'Subscriber Info.FirstName': name[0],
                    'Subscriber Info.LastName': name[1],
                    'email': random_email,
                    'Subscriber Info.StoreState': 'North Carolina',
                    'Subscriber Info.StoreZip': '40040',
                    'Subscriber Info.StoreCity': 'Rockingham',
                    'Subscriber Info.StoreCode': '189',
                    'DatePart.MonthPart.Subscriber Info.DOB': '10',
                    'DatePart.DayPart.Subscriber Info.DOB': '01',
                    'DatePart.YearPart.Subscriber Info.DOB': str(random.randint(1950, 1999)) ,
            }

            try:
                response = await session.post('https://enews.captainds.com/q/kENdj8EWmenSHZtzPGsNvRnrVNQY9n9pZ_bznBAZfcn4SwaKVlpsgXSKl', 
                    headers=headers, data=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.captainds_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "Welcome" in result:
            embed = discord.Embed(title="C̷a̷p̷t̷a̷i̷n̷ D̷s̷", url="https://captainds.com",
                description=f"Check email for a **free 1pc fish and fries**.\n\n"
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
            return await command_error(self, ctx, botmsg, self.bot.captainds_cd, cogname, connector, "BadResponse")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(captainds(bot))
