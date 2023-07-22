from helper import *

cogname = "everyplate"
class everyplate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.everyplate_cd = []
        bot.global_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                          description = f"50% discount")   
    async def everyplate(self, ctx: commands.Context):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.everyplate_cd)

        await check_roles(ctx, role_id)

        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating discount...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        random_email = await check_emails(self, ctx)

        connector = ProxyConnector.from_url(f'http://bqiqgfuj:mO0UqvI1fl@108.165.230.{str(random.randint(80, 104))}:3486')

        scraper = cloudscraper.create_scraper()

        headers= {
            "User-Agent": random.choice(self.bot.user_agents)
            }
            
        data = {
                'password': 'Suicideshots310!',
                'username': 'saywhu@smartnator.com'
                }

        try:
            response = scraper.post('https://www.everyplate.com/gw/login?country=ER&locale=en-US', 
                json=data, headers=headers, timeout=20)
        except:
            print(f"RequestTimeout: {cogname}(user_id:{ctx.author.id}, ip: {connector._proxy_host}:{connector._proxy_port}")
            await command_error(self, ctx, botmsg, self.bot.everyplate_cd)
        
        result = await response.text()
        print(result)

                
        result = response.json()
        print(result)
        token = result['access_token']

        async with CloudflareScraper() as session:
            headers = {
                    "User-Agent": random.choice(self.bot.user_agents),
                    'Authorization': f'Bearer {token}'
                }

            data = {
                    'referee_email': random_email,
                    'shared_platform': 'web',
                    'customer_id': 6779512,
                    'customer_full_name': 'mike sass',
                    'locale': 'en-US',
                }

            try:    
                response = await session.post('https://www.everyplate.com/gw/everyshare/referrals', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                print(f"RequestTimeout: {cogname}(user_id:{ctx.author.id}, ip: {connector._proxy_host}:{connector._proxy_port}")
                await command_error(self, ctx, botmsg, self.bot.everyplate_cd)

            result = response.headers['Content-Length']
            #print(result)            

        if result == "2":   
            if "yopmail" in random_email:
                embed = discord.Embed(title="E̷v̷e̷r̷y̷ P̷l̷a̷t̷e̷", url="https://www.everyplate.com/",
                    description= f"Check email for a **50% discount**.\n\n"
                            "Choose 2 people, 3 recipes plan. (50% discount)\n\n"
                          f"[Click here](https://yopmail.com/en/?login={random_email}) or go to https://yopmail.com\n\n" #edit
                            "Cancel subscription after delivery.\n"
                            "Use Vcc/jig address to create multiple accounts.")
            else:
                embed = discord.Embed(title="E̷v̷e̷r̷y̷ P̷l̷a̷t̷e̷", url="https://www.everyplate.com/",
                    description= f"Check email for a **50% discount**.\n\n"
                            "Choose 2 people, 3 recipes plan. (50% discount)\n\n"
                            "Cancel subscription after delivery.\n"
                            "Use Vcc/jig address to create multiple accounts.")

            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)

            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, None)

        else:
            async with aiofiles.open(f'Foodbot\\logs\\{cogname}.txt', mode="a") as f:
                await f.write(f"data: {data}\n----------\nresult: {result}\n----------\n\n")
                
            print(f"BadResponse: {cogname}(user_id:{ctx.author.id}, ip: {connector._proxy_host}:{connector._proxy_port}")
            await command_error(self, ctx, botmsg, self.bot.everyplate_cd)
        
        
async def setup(bot: commands.Bot):
    await bot.add_cog(everyplate(bot))
