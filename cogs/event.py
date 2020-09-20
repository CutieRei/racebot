import discord, aiosqlite, datetime
sql = aiosqlite
from discord.ext import commands,tasks
from discord.ext.commands import (CommandError,
    MissingRequiredArgument,
    BadArgument,
    PrivateMessageOnly,
    NoPrivateMessage,
    CheckFailure,
    CheckAnyFailure,
    CommandNotFound,
    DisabledCommand,
    CommandInvokeError,
    TooManyArguments,
    UserInputError,
    CommandOnCooldown,
    MaxConcurrencyReached,
    NotOwner,
    MissingRole,
    BotMissingRole,
    MissingAnyRole,
    BotMissingAnyRole,
    MissingPermissions,
    BotMissingPermissions,
    NSFWChannelRequired,
    ConversionError,
    BadUnionArgument,
    ArgumentParsingError,
    UnexpectedQuoteError,
    InvalidEndOfQuotedStringError,
    ExpectedClosingQuoteError,
    ExtensionError,
    ExtensionAlreadyLoaded,
    ExtensionNotLoaded,
    NoEntryPointError,
    ExtensionFailed,
    ExtensionNotFound,)

class Events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[{datetime.datetime.now()}][Events] Bot Ready")
    
    @commands.Cog.listener()
    async def on_disconnect(self):
        print(f"[{datetime.datetime.now()}][Events] Bot Disconnected")
    
    @commands.Cog.listener()
    async def on_command_error(self,ctx,err):
        if hasattr(ctx.command,'on_error'):
            return
        if isinstance(err,CommandNotFound):
            return
        elif isinstance(err,MissingRequiredArgument):
            await ctx.send(f'Missing required **{err.param.name}**')
        elif isinstance(err,BadArgument):
            await ctx.send("You gave wrong argument type!")
        elif isinstance(err,PrivateMessageOnly):
            await ctx.send("You can only run this command in DM")
        elif isinstance(err,NoPrivateMessage):
            await ctx.send('You cant use this command in DM')
        elif isinstance(err,DisabledCommand):
            await ctx.send("Command is is disabled")
        elif isinstance(err,TooManyArguments):
            await ctx.send("You gave too many argument")
        elif isinstance(err,CommandOnCooldown):
            s,m,h = int(err.retry_after),0,0
            if s > 60:
                m += s//60
                s = s%(m*60)
            if m > 60:
                h += m//60
                m = m%(m*60)
            await ctx.send(f"You can use this command again after **{h}h {m}m {s}s** per {err.cooldowm.type.name.capitalize()}")
        """
        elif isinstance(err,MaxConcurrencyReached):
        elif isinstance(err,NotOwner):
        elif isinstance(err,MissingRole):
        elif isinstance(err,MissingAnyRole):
        elif isinstance(err,BotMissingRole):
        elif isinstance(err,BotMissingAnyRole):
        elif isinstance(err,NSFWChannelRequired):
        elif isinstance(err,ConversionError):
        elif isinstance(err,BadUnionArgument):
        elif isinstance(err,ArgumentParsingError):
        elif isinstance(err,UnexpectedQuoteError):
        elif isinstance(err,InvalidEndOfQuotedStringError):
        elif isinstance(err,ExpectedClosingQuoteError):
        elif isinstance(err,ExtensionError):
        elif isinstance(err,ExtensionAlreadyLoaded):
        elif isinstance(err,ExtensionNotLoaded):
        elif isinstance(err,NoEntryPointError):
        elif isinstance(err,ExtensionFailed):
        elif isinstance(err,ExtensionNotFound):
        """



def setup(bot):
    bot.add_cog(Events(bot))
    print(f"[{datetime.datetime.now()}][Events] Loaded")