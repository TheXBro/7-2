
from helper import *

cogname = "mcdonalds"
class mcdonalds(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.mcdonalds_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free large fries")   
    async def mcdonalds(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.mcdonalds_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx, "smartnator.com")
        password = None        
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)
        
        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                    'Accept': 'application/json',
                    'Accept-Language': 'en-US',
                    'Authorization': 'Basic OGNHY2tSNXdQZ1FuRkJjOWRlVmhKMnZUOTRXaE1CUkw6WW00clZ5cXBxTnBDcG1yZFBHSmF0UnJCTUhoSmdyMjY=',
                    'Cache-Control': 'true',
                    'Host': 'us-prod.api.mcd.com',
                    'User-Agent': 'MCDSDK/7.3.2 (iPad; 15.3; en-US) GMA/7.1.0',
                    'accept-charset': 'utf-8',
                    'mcd-clientid': '8cGckR5wPgQnFBc9deVhJ2vT94WhMBRL',
                    'mcd-clientsecret': 'Ym4rVyqpqNpCpmrdPGJatRrBMHhJgr26',
                    'mcd-marketid': 'US',
                    'mcd-sourceapp': 'GMA',
                    'mcd-uuid': '00ecfbb8-0114-4cfe-a3c5-d218cff97e51',
            }

            data = {
                    'grantType': 'client_credentials',
            }

            try:
                response = await session.post('https://us-prod.api.mcd.com/v1/security/auth/token', 
                    headers=headers, data=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.mcdonalds_cd, cogname, connector, "RequestTimeout")

            result = await response.json()
            token = result['response']['token']

            headers = {
                    'Accept-Language': 'en-US',
                    'Authorization': f'Bearer {token}',
                    'Cache-Control': 'true',
                    'Content-Type': 'application/json; charset=UTF-8',
                    'Host': 'us-prod.api.mcd.com',
                    'User-Agent': 'MCDSDK/23.0.15 (Android; 22; en-US) GMA/7.5.0',
                    'X-NewRelic-ID': 'UwUDUVNVGwcDUlhbDwUBVg==',
                    'X-acf-sensor-data': '1,a,VJOyyvbov7k3KVjMnxQ5wUyw1rU5ZCBwLSn3E+sx/tgozIW89ltTwe7Da+xpYPxE2yTkv+/FbrBQ51Jf/dD6tM4FcmkvpST7kAehOIY3Aj2fw5x98OtOngN9cQWq5pWs6Uo0DHg1rbe4i6hsazxp7nmtNwRWgtKgxwuM8l4PnGE=,qrQNks6QcTBNLcBV+aaxGugXcIeG9UMvoZOx9tGSlDMDSFeJOAuxrFc7HJQfS9u30ogGgjOh/35/FKFzkj04cYKeh2euDI5cEPPJS8akX7NsFQWtKhtaZEMxBI9Vq35DrWmmXDqBmFyV9Db/D741ux5Y5pdh8EYdy7PCd3LEQ20=$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$2000,1000,1000',
                    'mcd-clientid': '8cGckR5wPgQnFBc9deVhJ2vT94WhMBRL',
                    'mcd-marketid': 'US',
                    'mcd-sourceapp': 'GMA',
                    'mcd-uuid': 'f20d1f1d-bc51-4d4f-bcce-44a756bc3c00',
                    'newrelic': 'eyJ2IjpbMCwyXSwiZCI6eyJkLnR5IjoiTW9iaWxlIiwiZC5hYyI6IjczNDA1NiIsImQuYXAiOiI0MzY5OTg0NjAiLCJkLnRyIjoiMjE2YzMxOGU2YzZjNDQ1NGJmOTg1OWU4YjJjZjFmN2YiLCJkLmlkIjoiZjBlZTAwMzFkN2EzNDkyMSIsImQudGkiOjE2NTk3MzM0ODQ5MjB9fQ==',
            }

            data = {
                    'address': {
                        'country': 'US',
                        'zipCode': random_address.real_random_address()['postalCode'],
                    },
                    'audit': {
                        'registrationChannel': 'M',
                    },
                    'credentials': {
                        'loginUsername': random_email,
                        'sendMagicLink': True,
                        'type': 'email',
                    },
                    'device': {
                        'deviceId': f"9f{str(random.randint(1111, 9999))}f{str(random.randint(11111, 99999))}db20",
                        'deviceIdType': 'AndroidId',
                        'isActive': 'Y',
                        'os': 'android',
                        'osVersion': '5.1.1',
                        'pushNotificationId': 'e-03ZlgF_bI:APA91bGmx4a7606QFMQs7MlAYn7oRCqI73GoJPgwar7V2gjPzoBFadJ_aPdhkfh6zTOGbDxyloZU-VcdTdL8_aJ0rH4Dz5vT8hCDCuThXVD0sFMHNxw7fqJAE7UKDiQ4pUWMBZ__QJwz',
                        'timezone': 'America/Los_Angeles',
                    },
                    'emailAddress': random_email,
                    'firstName': name[0],
                    'lastName': name[1],
                    'optInForMarketing': True,
                    'policies': {
                        'acceptancePolicies': {
                            '1': True,
                            '4': True,
                            '5': False,
                            '6': False,
                        },
                    },
                    'preferences': [
                        {
                            'details': {
                                'mobileApp': 'en-US',
                                'email': 'en-US',
                            },
                            'preferenceId': 1,
                        },
                        {
                            'details': {
                                'mobileApp': 'Y',
                                'email': 'Y',
                            },
                            'preferenceId': 2,
                        },
                        {
                            'details': {
                                'mobileApp': 'Y',
                                'email': 'Y',
                            },
                            'preferenceId': 3,
                        },
                        {
                            'details': {
                                'mobileApp': 'Y',
                                'email': 'Y',
                            },
                            'preferenceId': 4,
                        },
                        {
                            'details': {
                                'mobileApp': 'Y',
                                'email': 'Y',
                            },
                            'preferenceId': 6,
                        },
                        {
                            'details': {
                                'mobileApp': 'Y',
                                'email': 'Y',
                            },
                            'preferenceId': 7,
                        },
                        {
                            'details': {
                                'mobileApp': 'Y',
                                'email': 'Y',
                            },
                            'preferenceId': 8,
                        },
                        {
                            'details': {
                                'mobileApp': 'Y',
                                'email': 'Y',
                            },
                            'preferenceId': 9,
                        },
                        {
                            'details': {
                                'mobileApp': 'Y',
                                'email': 'Y',
                            },
                            'preferenceId': 10,
                        },
                        {
                            'details': {
                                'mobileApp': [
                                    4,
                                    5,
                                ],
                                'email': [
                                    1,
                                    2,
                                    3,
                                ],
                            },
                            'preferenceId': 11,
                        },
                        {
                            'details': {
                                'enabled': 'Y',
                            },
                            'preferenceId': 12,
                        },
                        {
                            'details': {
                                'enabled': 'Y',
                            },
                            'preferenceId': 13,
                        },
                        {
                            'details': {
                                'enabled': 'Y',
                            },
                            'preferenceId': 14,
                        },
                        {
                            'details': {
                                'enabled': 'Y',
                            },
                            'preferenceId': 15,
                        },
                        {
                            'details': {
                                'enabled': 'Y',
                            },
                            'preferenceId': 16,
                        },
                        {
                            'details': {
                                'enabled': 'Y',
                            },
                            'preferenceId': 17,
                        },
                        {
                            'details': {
                                'enabled': 'Y',
                            },
                            'preferenceId': 18,
                        },
                        {
                            'details': {
                                'enabled': 'Y',
                            },
                            'preferenceId': 19,
                        },
                        {
                            'details': {
                                'enabled': 'Y',
                            },
                            'preferenceId': 20,
                        },
                        {
                            'details': {
                                'enabled': 'Y',
                            },
                            'preferenceId': 21,
                        },
                        {
                            'details': {
                                'enabled': 'Y',
                            },
                            'preferenceId': 22,
                        },
                    ],
                    'subscriptions': [
                        {
                            'optInStatus': 'Y',
                            'subscriptionId': '1',
                        },
                        {
                            'optInStatus': 'Y',
                            'subscriptionId': '2',
                        },
                        {
                            'optInStatus': 'Y',
                            'subscriptionId': '3',
                        },
                        {
                            'optInStatus': 'Y',
                            'subscriptionId': '4',
                        },
                        {
                            'optInStatus': 'Y',
                            'subscriptionId': '5',
                        },
                        {
                            'optInStatus': 'Y',
                            'subscriptionId': '7',
                        },
                        {
                            'optInStatus': 'Y',
                            'subscriptionId': '10',
                        },
                        {
                            'optInStatus': 'Y',
                            'subscriptionId': '11',
                        },
                        {
                            'optInStatus': 'Y',
                            'subscriptionId': '24',
                        },
                        {
                            'optInStatus': 'Y',
                            'subscriptionId': '25',
                        },
                    ],
            }

            try:
                response = await session.post('https://us-prod.api.mcd.com/exp/v1/customer/registration', 
                    headers=headers, json=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.mcdonalds_cd, cogname, connector, "RequestTimeout")
            
            result = await response.text()

        if "Success" in result:
            embed = discord.Embed(title="M̷c̷d̷o̷n̷a̷l̷d̷s̷", url="https://www.mcdonalds.com",
                description=f"Verify email for **free large fries**.\n\n"
                            "No purchase necessary. Redeem online or in-store.")

            if "smartnator" in random_email:
                embed.add_field(name=f"email", value=f"[{random_email}](https://www.emailnator.com/inbox/{random_email})", inline=False)
            else:
                embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)

            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            await command_error(self, ctx, botmsg, self.bot.mcdonalds_cd, cogname, connector, "BadResponse")
               
async def setup(bot: commands.Bot):
    await bot.add_cog(mcdonalds(bot))
