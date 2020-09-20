import discord,random, datetime
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @staticmethod
    def rand_col():
        return discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
    def syntax(self,cmd):
        help = cmd.help or "No description"
        alias = [cmd.qualified_name]
        alias.extend([al for al in cmd.aliases])
        alias = "|".join(alias)
        brief = cmd.brief
        argument = cmd.signature
        return (help,alias,brief,argument)
    
    @commands.command(brief="Show this!")
    async def help(self,ctx,*,command=None):
        """
        Show this!
        """
        if command:
            cmd = self.bot.get_command(command)
            if cmd:
                if cmd.hidden:
                    await ctx.send("That command doesn't exists")
                    return
                syntax = self.syntax(cmd)
                embed = discord.Embed(colour=self.rand_col(),title=f"Help for {cmd.qualified_name}", description=f"```{syntax[1]} {syntax[3]}```", timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=ctx.author.avatar_url)
                embed.add_field(name="Description",value=syntax[0],inline=False)
                groups = getattr(cmd,"commands",None)
                if groups:
                    sub = []
                    count = 1
                    for name in groups:
                        sub.append(f"`{count}. {name.name}   {name.brief or ''}`")
                        count += 1
                    embed.add_field(name="Subcommands",value="\n".join(sub),inline=False)
                await ctx.send(embed=embed)
                return
            await ctx.send("That command doesn't exists")
            return
        embed = discord.Embed(title="Help list", description="Show list of commands", timestamp=datetime.datetime.utcnow(),colour=self.rand_col())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        cogs = []
        for name,i in self.bot.cogs.items():
            if [a for a in i.walk_commands()]:
                cogs.append(name)
        categories = {cog:[] for cog in cogs}
        categories["Uncategorized"] = []
        for cmd in self.bot.commands:
            if not cmd.hidden:
                categories[cmd.cog_name or "Uncategorized"].append(cmd)
        for cog,cmds in categories.items():
            embed.add_field(name=cog,value="\n".join([f"{cmd.name}   {cmd.brief or ''}" for cmd in cmds]) or "No commands",inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
    print(f"[{datetime.datetime.now()}][Help] Loaded")