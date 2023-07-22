from helper import *


class food(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name = "food",
                          description = "View available commands")    
    #@app_commands.checks.has_any_role() #add roles here
    async def food(self, ctx: commands.Context):
        embed = discord.Embed(description=

            "</everyplate:1029271178717700104> - 50% discount\n"
            "</factor75:1029271178717700102> - 50% discount\n"
            #"every plate - `.every`\n"
            #"hello fresh - `.hello`\n"
            #"**factor** - factor75 $40 off\n"                                                                    
            #"**restaurant** - restaurant.com $100 credit\n"
            #"**</arbys:1007141072281022515>** - Free classic roast beef (w/ any purchase)\n"
            "**</arbys:1029269557703082075>** - Free classic roast beef or slider (w/ purchase)\n"
            #"**aw** - Free root beer\n"
            "**</bjs:1029271178789003306>** - Free Pizookie dessert\n"
            "**</bojangles:1029271178717700103>** - Free 2pc leg & thigh meal and drink\n"
            "**</capizzakitchen:1029271178755444763>** - Free small plate and $5 reward\n"
            "**</captainds:1029271178755444764>** - Free fish and fries\n"
            #"**checkers / rallys** - Free Big Buford or Mother Cruncher\n"                                                                    
            "**</chilis:1029271178789003309>** - Free chips & salsa or non-alcoholic drink\n"
            "**</deltaco:1029271178789003308>** - Free shake and 2 free Del Tacos\n"
            "**</dennys:1029271178789003310>** - Free Everyday Value Slam breakfast\n"
            "**</einsteinbros:1029271178755444759>** - Free bagel and coffee (w/ purchase)\n"
            #"**elpolloloco** - Free chips and guac\n"
            "**</firehousesubs:1029271178717700096>** - Free medium sub\n"
            "**</freddys:1029271178717700100>** - Free double burger or frozen custard & Oreo sandwich\n"
            "**</gregoryscoffee:1029271178717700101>** - Free any drink\n"
            #"**halalguys** - Free side and drink (w/ entree purchase)\n"
            "**</krispykreme:1029271178717700098>** - Free dozen glazed donuts\n"
            #"**kungfutea** - Free $2 reward\n"
            "**</littlebigburger:1029271178789003315>** - Free root beer float\n"
            "**</mcdonalds:1029271178826752010>** - Free large fries\n"
            #"**ocharleys** - Free appetizer\n" #🔴
            "**</panera:1029271178755444762>** - Free pastry or sweet treat (w/ purchase)\n"
            "**</pollocampero:1029271178717700105>** - Free $10 reward\n"
            #"**qdoba** - Free chips and queso (w/ entree purchase)\n"
            "**</redrobin:1029271178789003307>** - Free custom burger\n"
            "**</rubios:1029271178717700097>** - Free $5 reward and BOGO free entree\n"
            "**</salsaritas:1029271178789003314>** - Free any entree\n"
            "**</smoothieking:1029271178717700099>** - Free $2 reward and espresso shot\n"
            "**</steaknshake:1029271178755444758>** - Free specialty shake\n"
            #"**tacobell** - Free Doritos Locos taco\n"
            #"**tgifridays** - Free chips & salsa, dessert or snack\n" #🔴
            "**</wafflehouse:1029271178789003311>** - Free 2 topping hashbrown\n"
            "**</wendys:1029271178755444757>** - Free cheeseburger or 10 pc nuggets (w/ any purchase)\n"
            #"**whataburger** - Free burger\n"
            "**</whitecastle:1029271178755444756>** - Free dessert on a stick\n"
            "**</wienerschnitzel:1029271178789003313>** - Free chili dog\n"
            "**</yoshinoya:1029271178755444765>** - Free regular bowl (w/ drink purchase)\n"
            "\n Set catchall to account - </catchall:1029319768576114689> **example.com**"
            f"\n Pass a name to command | example - </bjs:0> **{names.get_full_name()}**"
            #"\n• Type `/` to use <@945897617152438283> slash commands."
        )
        
        embed.set_author(name= "Food commands:")
        await ctx.send(embed = embed)
            
async def setup(bot: commands.Bot):
    await bot.add_cog(food(bot))
