from helper import *

cogname = "wienerschnitzel"
class wienerschnitzel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.wienerschnitzel_cd = []
        bot.add_view(PersistentView())

    @commands.hybrid_command(name = cogname,
                             description = "Free chili dog")   
    async def wienerschnitzel(self, ctx: commands.Context, name: Optional[str]):
        await ctx.defer()

        await check_cooldowns(self, ctx, cogname, self.bot.wienerschnitzel_cd)

        await check_roles(ctx, role_id)

        random_email = await check_emails(self, ctx)
        password = None
        phonenumber = f"(917) {str(random.randint(2, 9))}" + str(random.randint(11, 99)) + "-" + str(random.randint(1111, 9999))
        name = await check_name(ctx, name)
        
        embed = discord.Embed(description=f"You'll receive a DM when ready.")
        embed.set_author(name="Generating account...", icon_url="https://i.ibb.co/rkr737h/loading.gif")
        botmsg = await ctx.reply(embed=embed)

        connector = ProxyConnector.from_url(proxies())
        async with CloudflareScraper(connector=connector) as session:
            headers = {
                        'Host': 'www.wienerschnitzel.com',
                        'Origin': 'https://www.wienerschnitzel.com',
                        'Content-Type': 'multipart/form-data; boundary=---------------------------37444494421843881822771955150',
                        'User-Agent': random.choice(self.bot.user_agents),
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                        'Referer': 'https://www.wienerschnitzel.com/join/',
                        'Accept-Language': 'en-US,en;q=0.9',
                    }
                    
            bday1 = datetime.datetime.today().strftime('%m').lstrip("0").replace(" 0", " ")
            bday2= datetime.datetime.today().strftime('%d').lstrip("0").replace(" 0", " ")
            bday3= str(random.randint(1950, 1999))
            zip = random_address.real_random_address()['postalCode']
            data = f'-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="input_6"\r\n\r\n{name[0]}\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="input_7"\r\n\r\n{name[1]}\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="input_2"\r\n\r\n{random_email}\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="input_9"\r\n\r\n{phonenumber}\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="input_4[]"\r\n\r\n{bday1}\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="input_4[]"\r\n\r\n{bday2}\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="input_4[]"\r\n\r\n{bday3}\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="input_10"\r\n\r\nYes\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="input_5"\r\n\r\n{zip}\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="gform_ajax"\r\n\r\nform_id=1&title=&description=&tabindex=49\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="is_submit_1"\r\n\r\n1\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="gform_submit"\r\n\r\n1\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="gform_unique_id"\r\n\r\n\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="state_1"\r\n\r\nWyJbXSIsIjVmMGY5YmE3YTg0ZDBiZjZkZGYxMjY3Y2E1YTMzZjQyIl0=\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="gform_target_page_number_1"\r\n\r\n0\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="gform_source_page_number_1"\r\n\r\n1\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="gform_field_values"\r\n\r\n\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_hp_textarea"\r\n\r\n\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_js"\r\n\r\n1664090526869\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bib"\r\n\r\n1664090529240\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bfs"\r\n\r\n1664090565608\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bkpc"\r\n\r\n49\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bkp"\r\n\r\n122;80,91;110,55;44,101;120;130,90;85,70;156,30;109,92;180;160,125;35,91;26,10;105,104;45,80;106,5;136,40;101,15;180,50;71,105;120,150;99,718;87,24;70,52;77,103;106,30;71,70;94,121;106,75;114,11;90,5;78,46;110;101,20;76,395;80,305;97,70;80,19;69,176;80,91;70,155;55,176;91;135,134;146,391;104,1755;95,1128;80,111;311,2868;\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bmc"\r\n\r\n96;90,230;81,10046;53,1779;74,407;0,4585;64,394;0,2167;130,493;83,141;1,931;78,406;81,151;78,14707;\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bmcc"\r\n\r\n14\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bmk"\r\n\r\n20;47\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bck"\r\n\r\n13;13\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bmmc"\r\n\r\n17\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_btmc"\r\n\r\n0\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bsc"\r\n\r\n6\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bte"\r\n\r\n\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_btec"\r\n\r\n0\r\n-----------------------------37444494421843881822771955150\r\nContent-Disposition: form-data; name="ak_bmm"\r\n\r\n337,50;679,11;2255,323;294,8;105,36;21,40;815,28;489,124;2,51;655,238;707,110;230,660;944,1587;195,1616;369,1735;257,281;497,700;\r\n-----------------------------37444494421843881822771955150--\r\n'                
            try:
                response = await session.post('https://www.wienerschnitzel.com/join/#gf_1', 
                    headers=headers, data=data, ssl=False, timeout=20)
            except:
                return await command_error(self, ctx, botmsg, self.bot.wienerschnitzel_cd, cogname, connector, "RequestTimeout")

            result = await response.text()

        if "thank-you" in result:
            embed = discord.Embed(title="W̷i̷e̷n̷e̷r̷s̷c̷h̷n̷i̷t̷z̷e̷l̷", url="https://www.wienerschnitzel.com/food/hot-dogs/chili-dog/",
                description=f"Check email for a **free chili dog**.\n\n"
                            "No purchase necessary. Scan in-store to redeem.")

            if "yopmail" in random_email:
                embed.add_field(name=f"email", value=f"[{random_email}](https://yopmail.com/en/?login={random_email})", inline=False)
            else:
                embed.add_field(name=f"email", value=f"`{random_email}`", inline=False)

            user = self.bot.get_user(ctx.author.id)
            msg = await user.send(embed=embed, view=PersistentView())                                
                       
            newembed = discord.Embed(description=f"Check DMs. {ctx.author.mention}")
            newembed.set_author(name="Success!")
            await botmsg.edit(embed=newembed)

            await update_database(self, ctx, cogname, msg.id, random_email, password)

        else:
            return await command_error(self, ctx, botmsg, self.bot.wienerschnitzel_cd, cogname, connector, "BadResponse")

async def setup(bot: commands.Bot):
    await bot.add_cog(wienerschnitzel(bot))
