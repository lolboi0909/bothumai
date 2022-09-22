import discord, os
import cogs
from dotenv import load_dotenv
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from typing import Literal, Optional

load_dotenv(r'secure.env')


TOKEN = 'MTAxOTI2MzI2NzcwNjc4NTkwMg.GfHhd8.SjGGYKhyfs8cnZhu12gddCFQhyGodYUKsqqZiY'

class discordbot(commands.Bot):
    
    def __init__(self):
        super().__init__(
            command_prefix="!", 
            intents=discord.Intents.all(),
            application_id=1019263267706785902,
            activity = discord.Activity(type=discord.ActivityType.listening, name="PMHUB OP!!"),
            help_command=None 
        )
        self.synced = False   
    


    async def setup_hook(self):
        await self.load_extension(f"cogs.feedback")
        await self.load_extension(f"cogs.blacklist")
        await self.load_extension(f"cogs.lookup")
        await self.load_extension(f"cogs.coupon")
        await self.load_extension(f"cogs.redeem")
    
        @bot.command()
        @commands.guild_only()
        @commands.is_owner()
        async def sync(
        ctx: Context, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
            if not guilds:
                if spec == "~":
                    synced = await ctx.bot.tree.sync(guild=ctx.guild)
                elif spec == "*":
                    ctx.bot.tree.copy_global_to(guild=ctx.guild)
                    synced = await ctx.bot.tree.sync(guild=ctx.guild)
                elif spec == "^":
                    ctx.bot.tree.clear_commands(guild=ctx.guild)
                    await ctx.bot.tree.sync(guild=ctx.guild)
                    synced = []
                else:
                    synced = await ctx.bot.tree.sync()

                await ctx.send(
                    f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
                )
                return

            ret = 0
            for guild in guilds:
                try:
                    await ctx.bot.tree.sync(guild=guild)
                except discord.HTTPException:
                    pass
                else:
                    ret += 1

            await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
    
    async def on_ready(self):
        return

bot = discordbot()
bot.run(TOKEN)
