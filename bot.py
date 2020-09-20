import discord,aiosqlite
sql = aiosqlite
from discord.ext import commands

bot = commands.Bot(command_prefix="rc.",help_command=None)
bot.load_extension('jishaku')
bot.owner_ids = [452745892718575616,716503311402008577]
for ext in ["cogs.game","cogs.event","cogs.help"]:
    bot.load_extension(ext)

@bot.event
async def on_message(msg):
    if msg.author.bot:
        pass
    else:
        async with sql.connect("./db/data.sql") as db:
            async with db.execute("SELECT * FROM users WHERE id = ?",(msg.author.id,)) as c:
                user = await c.fetchone()
                if not user:
                    await db.execute("INSERT INTO users (id) VALUES (?)",(msg.author.id,))
                    await db.commit()
                else:
                    exp = user[4]
                    if exp > 2000:
                        exp = 2000
                    level = exp//100
                    await db.execute('UPDATE users SET level = ?,exp = ? WHERE id = ?',(level,exp,msg.author.id,))
                    await db.commit()
    await bot.process_commands(msg)


token = None
with open('private/token.txt',"r") as file:
    token = file.read()
bot.run(token)