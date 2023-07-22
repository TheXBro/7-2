from helper import *
import nest_asyncio

nest_asyncio.apply()

cogname = "arbys"
class arbys(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.arbys_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free classic roast beef and slider")   
    async def arbys(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()
                      
        await check_cooldowns(self, ctx, cogname, self.bot.arbys_cd)

        await check_roles(ctx, role_id)
        
        random_email = await check_emails(self, ctx)
        password =  await gen_password()
        phonenumber = f"917{str(random.randint(2, 9))}" + str(random.randint(111111, 999999))  
        name = await check_name(ctx, name)
        print(name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)
    
        connector = ProxyConnector.from_url(proxies())
        print(connector)
        async with CloudflareScraper(connector=connector) as session:
            print(session)
            headers = {
                'User-Agent': random.choice(self.bot.user_agents),
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.5',
                'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjI4NzkyOTAiLCJhcCI6IjkxMTEzNjQ0NiIsImlkIjoiNWRhYzU3ZDhhYTc2M2Q3ZCIsInRyIjoiYjgyMzAzYmI4N2M4MmY5NjA4OWQyNDdmZGI3YTY1ODAiLCJ0aSI6MTY1OTE2ODgzNTU4NH19',
                'traceparent': f'00-b82303bb87c82f96089d247fdb7a6580-5dac57d8aa763d7d-0{random.randint(1, 9)}',
                'tracestate': f'2879290@nr=0-1-2879290-911136446-5dac57d8aa763d7d----{random.randint(1111111111111, 9999999999999)}',
                'Auth0-Client': 'eyJuYW1lIjoiYXV0aDAuanMiLCJ2ZXJzaW9uIjoiOS4xNi40In0=',
                'Origin': 'https://login.arbys.com',
                'Alt-Used': 'login.arbys.com',
            }
            print(headers)

            data = {
                'client_id': 'ZfKuQMgYC4iD3iUKE3zmYgxh2cadxnOU',
                'state': 'hKFo2SBEOWFSZDdiRzRPa2tmbjNkRWx5aEJlVmtuX3lBamprMKFupWxvZ2luo3RpZNkgY3B0SEFCVWhJN0RWNlo2OUNTREpBZFN0MC1RTnRqcU6jY2lk2SBaZkt1UU1nWUM0aUQzaVVLRTN6bVlneGgyY2FkeG5PVQ',
                'connection': 'firebase-auth',
                'email': random_email,
                'password': password,
                'given_name': name[0],
                'family_name': name[1],
                'user_metadata': {
                    'birthDate': '11-01',
                    'zipCode': random_address.real_random_address()['postalCode'],
                    'phone': phonenumber,
                    'termsLink': 'https://www.arbys.com/terms-of-use',
                    'termsAcceptedAt': f"2022-{datetime.datetime.now().strftime('%m')}-{datetime.datetime.now().strftime('%d')}T{datetime.datetime.now().strftime('%H')}:{str(random.randint(11, 99))}:{str(random.randint(11, 99))}.{str(random.randint(111, 999))}Z",
                    'marketingOptIn': 'on',
                },
            }
            
            print(data)


            response = await session.post('https://login.arbys.com/dbconnections/signup', 
                    headers=headers, json=data, ssl=False, timeout=20)



            result = await response.text()
            print(result)

        print(random_email)
        if random_email in result:
            embed = discord.Embed(title="A̷r̷b̷y̷s̷​", url="https://www.arbys.com/",
                description= f"Login app or site for a **free Classic roast beef** or **free slider**.\n\n"
                            "Any purchase required. Redeem online or in-store.")
            embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)
            embed.add_field(name='password', value=f"`{password}`",inline=False)
            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            return await command_error(self, ctx, botmsg, self.bot.arbys_cd, cogname, connector, "BadResponse")

async def setup(bot: commands.Bot):
    await bot.add_cog(arbys(bot))
