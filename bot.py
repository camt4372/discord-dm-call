import discord
from discord.ext import commands
import asyncio
import time

TOKEN = "" # 봇 토큰 넣어요

intents = discord.Intents.default()
intents.members = True
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)



cooldowns = {}
COOLDOWN_SECONDS = 60  # 쿨타임 임다 지금은 60초
restricted = False

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        if message.content.startswith('!'):
            embed = discord.Embed(title="오류", description="봇 디엠으로는 명령어를 사용하실 수 없습니다.", color=discord.Color.red())
            await message.channel.send(embed=embed)
    else:
        await bot.process_commands(message)


@bot.command()
@commands.is_owner()
async def 제한(ctx):
    global restricted
    restricted = True
    embed = discord.Embed(title="제한됨", color=discord.Color.red())
    await ctx.reply(embed=embed)

@bot.command()
@commands.is_owner()
async def 허용(ctx):
    global restricted
    restricted = False
    embed = discord.Embed(title="허용됨", color=discord.Color.green())
    await ctx.reply(embed=embed)

@bot.command()
async def 호출(ctx):
    user_id = 719918521307496559 # 호출될사람 아이디 적어요. 예를들면 사장 아디 넣으삼
    author_id = ctx.author.id
    channel_id = ctx.channel.id

    # Check if restricted
    if restricted:
        embed = discord.Embed(title="사용제한", description="관리자가 사용을 중지시켰습니다.", color=discord.Color.red())
        await ctx.reply(embed=embed)
        return

    # Check if the user is in cooldown
    if author_id in cooldowns:
        remaining_seconds = int(cooldowns[author_id] - time.time())
        if remaining_seconds > 0:
            embed = discord.Embed(title="쿨타임", description=f"{remaining_seconds}초 남았습니다. 잠시 후 사용하세요.", color=discord.Color.red())
            await ctx.reply(embed=embed)
            return

    # If not in cooldown, reset the cooldown time
    cooldowns[author_id] = time.time() + COOLDOWN_SECONDS

    user = await bot.fetch_user(user_id)

    dm_message = f"<@{author_id}>님이 <#{channel_id}>에서 호출하셨습니다."
    
    try:
        # Send DM to the specified user
        await user.send(dm_message)

        # Send message to the channel
        embed = discord.Embed(title="성공적으로 호출됨", description=f"<@{author_id}>님, 호출 하였습니다. 잠시만 기다려주세요.", color=discord.Color.green())
        await ctx.reply(embed=embed)
    except discord.HTTPException:
        await ctx.reply("호출에 실패했습니다. 다시 시도해주세요.")

bot.run(TOKEN)