from helper import *

class catchall(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name = "catchall",
                          description = "Set catchall email to account")
    async def catchall(self, interaction: discord.Interaction, catchall: str):
        await interaction.response.defer(ephemeral=True)
        
        if ("@" in catchall)  or ("yopmail" in catchall):
            embed = discord.Embed(description=f"Invalid catchall. <@{str(interaction.user.id)}>\n\n**Retry command:**\n```/catchall example.com```")
            embed.set_author(name="Oops! Something went wrong.")  
            await interaction.followup.send(embed=embed)
            return

        if (".com" in catchall) or (".net" in catchall) or (".org" in catchall) or (".edu" in catchall) or (".net" in catchall) or (".co" in catchall) or (".xyz" in catchall) or (".io" in catchall):
            
            async with self.bot.db.cursor() as cursor:
                print(catchall)
                await cursor.execute(f"SELECT email FROM users WHERE user_id = {interaction.user.id}") 
                content = await cursor.fetchone()
                print(content)
                
                if content == None: 
                    await cursor.execute("INSERT OR REPLACE INTO users (user_id, email) VALUES (?,?)", (interaction.user.id, catchall,))  
                    await self.bot.db.commit()
                else:
                    await cursor.execute(f"UPDATE users SET email = ? WHERE user_id = ?", (catchall, interaction.user.id,))   
                    await self.bot.db.commit()
                
            embed = discord.Embed(description=f"Catchall set @ `{catchall}`")
            embed.set_author(name="Success!")
            await interaction.followup.send(embed=embed)


        else:
            embed = discord.Embed(description=f"Invalid catchall. <@{str(interaction.user.id)}>\n\n**Retry command:**\n```/catchall example.com```")
            embed.set_author(name="Oops! Something went wrong.")  
            await interaction.followup.send(embed=embed)

        
async def setup(bot: commands.Bot):
    await bot.add_cog(catchall(bot))
