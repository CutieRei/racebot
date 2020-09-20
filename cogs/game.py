import discord,json,random,aiosqlite,datetime
sql = aiosqlite
from discord.ext import commands

max_lvl_items = {
  "accelerator":20,
  "engine":20,
  "tires":20,
  "handling":20,
  "nitro":10
}

class Car:
    def __init__(self,car):
        car = json.loads(car)
        for item,lvl in car.items():
            max_lvl = max_lvl_items.get(item)
            if lvl > max_lvl:
                lvl = max_lvl
        self.engine = car.get('engine')
        self.nitro = car.get('nitro')
        self.tires = car.get('tires')
        self.handling = car.get('handling')
        self.accelerator = car.get('accelerator')
    
    def json(self):
        return {"engine": self.engine,"nitro":self.nitro,"tires":self.tires,"handling":self.handling,"accelerator":self.accelerator}
    
class Game(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def give(self,ctx,member:discord.Member,coin:int=0,exp:int=0):
        async with sql.connect("./db/data.sql") as db:
            async with db.execute("SELECT * FROM users WHERE id = ?",(member.id,)) as c:
                user = await c.fetchone()
                if not user:
                    await db.execute("INSERT INTO users (id) VALUES (?)",(msg.author.id,))
                    await db.commit()
                await db.execute('UPDATE users SET coin = coin + ?, exp = exp + ? WHERE id = ?',(coin,exp,member.id,))
                await db.commit()
        await ctx.send(f'Successfully gave **{coin} SquareCoin** and **{exp} Exp** to {member}')


    @commands.command(brief="Race with the bot")
    @commands.cooldown(1,5,commands.BucketType.user)
    @commands.max_concurrency(1,per=commands.BucketType.channel)
    async def play(self,ctx):
        """
        Race with the bot to with awesome prize
        """
        user_data = None
        car = None
        async with sql.connect("./db/data.sql") as db:
            async with db.execute('SELECT * FROM users WHERE id = ?',(ctx.author.id,)) as c:
                user = await c.fetchone()
                if not user:
                    await ctx.send('Something went wrong, please try again')
                    return
                user_data = user
                car = Car(user[3])
        def check(react,user):
            if str(react) in ["<:Nitro:753222811153072158>",'\U000025b6'] and user == ctx.author:
                return True
            return False
        track = random.uniform(user_data[2]*8,user_data[2]*10)
        win = False
        user = 0
        bot = 0
        nitro = False
        embed = discord.Embed(title=f'Race between {ctx.author} and {self.bot.user}',description="You're on the track",timestamp=datetime.datetime.utcnow(),colour=self.rand_col())
        embed.add_field(name="Bot progress",value=f"{str(bot)[:5]}/{str(track)[:5]}KM",inline=False)
        embed.add_field(name="User progress",value=f"{str(user)[:5]}/{str(track)[:5]}KM",inline=False)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("<:Nitro:753222811153072158>")
        await msg.add_reaction('\U000025b6')
        nitro_num = 0
        while not win:
            react = await self.bot.wait_for("reaction_add",check=check)
            progress = random.uniform(0,int(car.accelerator))
            if str(react[0]) == "<:Nitro:753222811153072158>":
                if nitro:
                    embed.description = 'You already used Nitro!'
                    await msg.edit(embed=embed)
                    await react[0].remove(ctx.author)
                    continue
                else:
                    nitro = True
                    nitro_temp = random.uniform(0,(car.nitro/2))
                    nitro_num = 1
                    progress += nitro_temp
            await react[0].remove(ctx.author)
            user += progress
            bot += random.uniform(0,int(car.accelerator))
            if bot > track:
                bot = float(track)
            if user > track:
                user = float(track)
            else:
                desc = f"You passed {str(progress)[:4]}KM"
                if nitro_num == 1:
                    desc = desc + ", and used nitro!"
                    nitro_num = 0
                embed.description = desc
            embed.set_field_at(0,name="Bot progress",value=f'{str(bot)[:5]}/{str(track)[:5]}KM',inline=False)
            embed.set_field_at(1,name="User progress",value=f'{str(user)[:5]}/{str(track)[:5]}KM',inline=False)
            await msg.edit(embed=embed)
            if user >= track or bot >= track:
                if user == bot:
                    win = None
                if user > bot:
                    win = True
                break
        coin,exp = 0,0
        embed.set_footer(icon_url=ctx.author.avatar_url,text='Game ended')
        if win:
            embed.description = "You win!"
            coin,exp =  [random.randint(10,15) for i in range(0,2)]
            await msg.edit(embed=embed)
        elif win is None:
            embed.description = "Tie"
            await msg.edit(embed=embed)
            await ctx.reinvoke()
        else:
            embed.description = "You lose!"
            coin,exp = [random.randint(0,5) for i in range(0,2)]
        async with sql.connect('./db/data.sql') as db:
            await db.execute('UPDATE users SET coin = coin + ?, exp = exp + ? WHERE id = ?',(coin,exp,ctx.author.id,))
            await db.commit()
        embed.add_field(name='Result',value=f"{coin} SquareCoin, {exp} Exp")
        await msg.edit(embed=embed)
    
    @play.error
    async def on_command_error(self,ctx,err):
        if isinstance(err,commands.MaxConcurrencyReached):
            await ctx.send('A game is already running in this channel, Running another one will conflict the current one!')
        elif isinstance(err,commands.CommandOnCooldown):
            s,m,h = int(err.retry_after),0,0
            if s > 60:
                m += s//60
                s = s%(m*60)
            if m > 60:
                h += m//60
                m = m%(m*60)
            await ctx.send(f"You can use this command again after **{h}h {m}m {s}s** per {err.cooldowm.type.name.capitalize()}")
        else:
            raise err

    @staticmethod
    def rand_col():
        return discord.Colour.from_rgb(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
    def check_admin(self,perms):
        if perms.kick_members or perms.administrator:
            return True
        return False
    
    @commands.command()
    async def test(self,ctx,engine:int,nitro:int,tires:int,handling:int, accelerator:int):
        """
        Test command
        """
        car = {"engine": engine,"nitro":nitro,"tires":tires,"handling":handling,"accelerator":accelerator}
        await ctx.send(Car(car).json())
        
        
    @commands.command(brief="Show profile", aliases=["p"])
    @commands.guild_only()
    async def profile(self,ctx,person: discord.Member=None):
        """
        Show profile of yourself or others.
        You need to have permission of kicking members to check other people profile
        """
        person = person or ctx.author
        if not self.check_admin(ctx.author.guild_permissions) and person:
            person = ctx.author
        async with sql.connect('./db/data.sql') as db:
            async with db.execute("SELECT * FROM users WHERE id = ?",(person.id,)) as c:
                user = await c.fetchone()
                if not user:
                    await ctx.send(":O something went wrong")
                    await db.execute('INSERT INTO users (id) VALUES (?)',(person.id,))
                    await db.commit()
                    return
                car = Car(user[3])
                embed = discord.Embed(title="Profile", description=f"Showing profile for **{person}**",colour=self.rand_col(), timestamp=datetime.datetime.utcnow())
                embed.add_field(name="SquareCoin",value=user[1],inline=False)
                embed.add_field(name="Levels",value=f"Level: **{user[2]}**\nExp: **{user[4]}**",inline=False)
                embed.add_field(name="Car",value=f"Engine lvl {car.engine}\nAccelerator lvl {car.accelerator}\nNitro lvl {car.nitro}\nTires lvl {car.tires}\nHandling lvl {car.handling}",inline=False)
                embed.set_footer(icon_url=person.avatar_url,text=person)
                embed.set_thumbnail(url=person.avatar_url)
                await ctx.send(embed=embed)
    
    @commands.group(invoke_without_command=True,brief="Show the shop")
    async def shop(self,ctx):
        """
        Show the shop
        """
        coin = 0
        async with sql.connect("./db/data.sql") as db:
            async with db.execute("SELECT * FROM users WHERE id = ?",(ctx.author.id,)) as c:
                coin = await c.fetchone()
                coin = coin[1]
        colour = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
        with open('./private/items.json','r') as data_file:
            data = json.load(data_file)
            embed = discord.Embed(title="The Shop",description="Upgrade your car attributes!",colour=discord.Colour.from_rgb(colour[0], colour[1],colour[2]),timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url="https://i.pinimg.com/originals/5d/78/18/5d78181296d8703acf634e7dd819fbc9.gif")
            embed.set_footer(icon_url=ctx.author.avatar_url,text=f"You have {coin} SquareCoin")
            for name,price in data.items():
                embed.add_field(name=name,value=f"Price: {price}",inline=False)
            await ctx.send(embed=embed)

    @shop.command(brief='Buy items')
    async def upgrade(self,ctx,item):
        item = item.lower()
        car,coin = None,0
        async with sql.connect('./db/data.sql') as db:
            async with db.execute('SELECT * FROM users WHERE id = ?',(ctx.author.id,)) as c:
                user = await c.fetchone()
                car = Car(user[3])
                coin = user[1]
        with open("./private/items.json",'r') as file:
            data = json.load(file)
            if not item in data:
                await ctx.send('Dude, that item doesn\'t exists')
                return
            car = car.json()
            if coin < data.get(item):
                await ctx.send('I\'m sorry but, you don\'t have enough SquareCoin.')
                return
            if car.get(item) >= max_lvl_items.get(item):
                await ctx.send(f'Dude, you already have max **{item}**')
                return
            coin -= data.get(item)
            car[item] += 1
            async with sql.connect('./db/data.sql') as db:
                await db.execute('UPDATE users SET coin = ?, car = ? WHERE id = ?',(coin,json.dumps(car),ctx.author.id,))
                await db.commit()
                await ctx.send(f'Successfully bought **{item}** for **{data.get(item)}**')


def setup(bot):
    bot.add_cog(Game(bot))
    print(f"[{datetime.datetime.now()}][Game] Loaded")
