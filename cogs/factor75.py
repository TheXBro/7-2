from helper import *

cogname = "factor75"
class factor75(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.factor_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = f"50% discount")   
    async def factor75(self, ctx: commands.Context):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.factor_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)

        connector = ProxyConnector.from_url(proxies())
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating discount...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        scraper = cloudscraper.create_scraper()

        headers= {
            "User-Agent": random.choice(self.bot.user_agents)
        }
            
        data = {
                'password': 'Suicideshots310!',
                'username': 'saywhu3@smartnator.com'
        }

        response = scraper.post('https://go.factor75.com/gw/login?country=FJ&locale=en-US', 
                json=data, timeout=5)

        try:
            response = scraper.post('https://go.factor75.com/gw/login?country=FJ&locale=en-US', 
                json=data, headers=headers, timeout=20)
        except:
            await command_error(self, ctx, botmsg, self.bot.factor_cd, cogname, connector, "RequestTimeout")

        result = response.json()
        token = result['access_token']

        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    "User-Agent": random.choice(self.bot.user_agents),
                    'Authorization': f'Bearer {token}'
            }

            data = {
                    'referee_email': random_email,
                    'shared_platform': 'web',
                    'customer_id': 4970177,
                    'customer_full_name': 'mike jones',
                    'locale': 'en-US',
            }

            try:    
                response = await session.post('https://go.factor75.com/gw/everyshare/referrals', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                await command_error(self, ctx, botmsg, self.bot.factor_cd, cogname, connector, "BadResponse")

            result = response.headers['Content-Length']

        if result == "2":   
            embed = discord.Embed(title="F̷a̷c̷t̷o̷r̷ 7̷5̷", url="https://www.factor75.com/",
                description= f"Check email for a **50% discount**.\n\n"
                             "Choose 4 meals plan. (50% discount)\n\n"
                             "Cancel subscription after delivery.\n"
                             "Use Vcc/jig address to create multiple accounts.")
            
            if "yopmail" in random_email:
                embed.add_field(name=f"email", value=f"[{random_email}](https://yopmail.com/en/?login={random_email})", inline=False)
            else:
                embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)

            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, None)

        else:
            await command_error(self, ctx, botmsg, self.bot.factor_cd, cogname, connector, "BadResponse")
        
async def setup(bot: commands.Bot):
    await bot.add_cog(factor75(bot))
