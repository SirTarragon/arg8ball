import discord
import random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @staticmethod
    def __ball_response() -> str:
        responses = ["It is certain.", "It is decidedly so.",
                     "Without a doubt. Yes definitely.",
                     "You may rely on it.", "As I see it, yes.",
                     "Most likely.", "Outlook good.", "Yes.",
                     "Signs point to yes.", "Reply hazy, try again.",
                     "Ask again later.", "Better not tell you now.",
                     "Cannot predict now.", "Concentrate and ask again.",
                     "Don't count on it.", "My reply is no.",
                     "My sources say no.", "Outlook not so good.",
                     "Very doubtful."]
        return responses[random.randint(0, len(responses) - 1)]

    @commands.hybrid_command(aliases=["coinflip", "flipcoin"])
    async def flip(self, ctx):
        """
        Flips a coin.
        Args:
            ctx (discord.ext.Context): The message Context.
        """
        heads_img = "https://media.discordapp.net/attachments/810007261530685461/1048046478293209138/heads.png"
        tails_img = "https://media.discordapp.net/attachments/810007261530685461/1048046478767169556/tails.png"
        rand = random.randint(0, 1)
        embed = discord.Embed(
            title="Coin Flip",
            description=f"You flipped a coin and got **{'Heads' if rand == 0 else 'Tails'}**!",
            color=discord.Color.blue()).set_image(
            url=heads_img if rand == 0 else 
            tails_img)
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=["diceroll", "rolldice"])
    async def roll(self, ctx, *, dice: str):
        """
        Rolls a (or multiple) dice. Format: [number of dice]d[number of sides]
        Args:
            ctx (discord.ext.Context): The message Context.
            dice (str): The dice to roll.
        """
        try:
            rolls, limit = map(int, dice.split("d"))
        except Exception as e:
            raise commands.BadArgument("Format has to be in NdN!") from e

        results = [random.randint(1, limit) for r in range(rolls)]
        embed = discord.Embed(
            title=f"Dice Roll {dice}",
            description=f"You rolled and got **{', '.join(str(result) for result in results)}**!\n" + \
            f"Total: **{sum(results)}**",
            color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.hybrid_command(aliases=["8ball", "8-ball", "eightball", "eight-ball"])
    async def ask(self, ctx, *, question: str):
        """
        Asks the magic 8-ball a question.
        Args:
            ctx (discord.ext.Context): The message Context.
            arg (str): The question to ask the 8ball.
        """
        try:
            embed = discord.Embed(
                title = f"\"{str(question)}\"",
                description=f"```{self.__ball_response()}```",
                color=discord.Color.blue())
            embed.set_image(url="https://emojipedia-us.s3.amazonaws.com/thumbs/120/twitter/134/billiards_1f3b1.png")
            await ctx.send(embed=embed)
        except Exception as e:
            raise commands.BadArgument("Please ask a question!") from e

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(embed=discord.Embed(
                title=":x: Error",
                description="Missing required argument(s).",
                color=discord.Color.red()))
        elif isinstance(error, commands.BadArgument):
            await ctx.send(embed=discord.Embed(
                title=":x: Error",
                description=str(error),
                color=discord.Color.red()))


async def setup(bot):
    await bot.add_cog(Fun(bot))