import discord
import os
import requests
import json
import random

# To ping to web server
from keep_alive import keep_alive

# for bot commands for invoking behaviors of bot
from discord.ext import commands

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='%', intents=intents)

# List of stuff of custom thinking Emoji

custom_thinking_list = [
    '<:ThinkingGrape:825352114821660702>', '<:thonk:824211395255337011>',
    '<:thinkzap:833040008515813426>',
    '<:thinkirby:824977141510307862>',
    '<:ThinkingLoaf:833042730128113705>',
    '<:PngItem_640782:829401912746835998>',
    '<:KiwiThink:833042762944217178>',
    '<:GWjustinTurtleThink:824209273587630091>',
    '<:BlurpleThonk:833040255015714847>', '<:ASTHETHINK:824974360686624769>',
    '<:9682thinksmug:823920596127580222>',
    '<:9166_Cool_Thinking_Blob:823920596203077665>',
    '<:7304_upsidedown_thinking:823920646467485697>',
    '<:7246_gayapple_think:829402652219408475>',
    '<:7128_thinktomato:829402318599880714>',
    '<:5928_Thinkxel:824977141540061204>',
    '<:3713_ThinkStarbucks:824977141539012648>',
    '<:1897clapthonk:823920646060900442>'
]

# --- bot command functions start here --- #

# -- Basic function for checking bot is working correctly


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


# --- Command for alerting server is on


@bot.command()
async def on(ctx):
    await ctx.send('@everyone :carrot::carrot::carrot::carrot::carrot:')


# --- Command for Emoji


@bot.command()
async def emo(ctx):
    random_idx = random.randint(0, len(custom_thinking_list) - 1)
    await ctx.send(custom_thinking_list[random_idx])


@bot.command()
async def emo_all(ctx):
    for idx in range(custom_thinking_list.__len__()):
        await ctx.send(custom_thinking_list[idx])


# --- Command for assigning role by user's reaction


@bot.command()
async def role_by_reaction(ctx):
    admin_id = 523433956906106880
    if ctx.message.author.id != admin_id:
        await ctx.send('This command is only available by administrator.')
    else:
        embed = discord.Embed(
            title='▬▬▬▬▬ [:star:] __**REACTION ROLE**__ ▬▬▬▬▬',
            description='> 아래의 리스트에서 원하는 색의 이모티콘을 누르고 자신의 이름에 원하는 색을 입혀봐!!',
            color=0xFF9B85, timestamp=ctx.message.created_at)

        # \nㅤ\n <= transparent letter and enter

        embed.add_field(
            name="**➥ 선택 가능한 역할 색 목록**",
            value="ㅤ\n 🌸 : <@&823883631318663180> \n\n 🍊 : <@&823882188985729084> \n\n 🍋 : <@&823883360668614686> \n\n 🍆 : <@&823882859198152724> \n\n 🌰 : <@&823884104617295912> \n\n 🥕 : <@&838454413948354570> \n\n 🍞 : <@&838456455757168680> \n\n 🍀 : <@&820436397420445706> \n\n 🧊 : <@&823882442238722079> \n\n <:Lime:838925395420119070> : <@&838193326817673277>ㅤ\nㅤ\n",
            inline=False)

        ava_url = ctx.author.avatar_url

        embed.set_footer(text=f'Made by {ctx.author}', icon_url=ava_url)

        msg = await ctx.send(embed=embed)

        await msg.add_reaction('🌸')
        await msg.add_reaction('🍊')
        await msg.add_reaction('🍋')
        await msg.add_reaction('🍆')
        await msg.add_reaction('🌰')
        await msg.add_reaction('🥕')
        await msg.add_reaction('🍞')
        await msg.add_reaction('🍀')
        await msg.add_reaction('🧊')
        await msg.add_reaction('<:Lime:838925395420119070>')

        await ctx.message.add_reaction('✅')


@bot.event
async def on_raw_reaction_add(payload):
    role_message_id = 840126617925451796

    if role_message_id == payload.message_id:
        member = payload.member
        guild = member.guild
        emoji = payload.emoji.name

        role = ''

        # if emoji == '❤️':
        # 	role = discord.utils.get(guild.roles, name='Pink')

        role = get_role(emoji, guild.roles)

        await member.add_roles(role)


@bot.event
async def on_raw_reaction_remove(payload):
    # on_raw_reaction_remove doesn't provide a member object
    role_message_id = 840126617925451796

    if role_message_id == payload.message_id:
        guild = await (bot.fetch_guild(payload.guild_id))
        member = await (guild.fetch_member(payload.user_id))
        emoji = payload.emoji.name

        role = ''

        # if emoji == '❤️':
        # 	role = discord.utils.get(guild.roles, name='Pink')

        role = get_role(emoji, guild.roles)

        await member.remove_roles(role)


def get_role(emoji, guild_roles):
    dic = {'🌸': 'Pink', '🍊': 'Orange', '🍋': 'Yellow', '🍆': 'Violet', '🌰': 'Cocoa',
           '🥕': 'Light salmon', '🍞': 'Wheat', '🍀': 'Green', '🧊': 'Sky blue', 'Lime': 'Lime'}

    role = discord.utils.get(guild_roles, name=dic[emoji])

    return role


# command for getting meme


def get_meme():
    random_idx = random.randint(0, 99)

    response = requests.get('https://api.imgflip.com/get_memes')
    json_data = json.loads(response.text)
    random_meme_object = json_data['data']['memes'][random_idx]
    meme_url = random_meme_object['url']
    return (meme_url)


@bot.command()
async def meme(ctx):
    meme_url = get_meme()
    await ctx.send(meme_url)


# ---


@bot.command()
async def babo(ctx):
    await ctx.send('yes 라면 y를 no라면 n을 입력해주세요')

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and \
            msg.content.lower() in ["y", "n"]

    msg = await bot.wait_for("message", check=check)
    if msg.content.lower() == "y":
        await ctx.send("You said yes!")
    else:
        await ctx.send("You said no!")


@bot.command()
async def roll(ctx):
    """Rolls a dice in NdN format."""
    await ctx.send(
        '주사위를 굴립니다. 몇번 굴릴지와 범위를 띄어쓰기로 구분해서 입력해주세요. 예시) 3번 굴리고, 범위는 1~6 => 3 6 이라고 입력'
    )

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    msg = await bot.wait_for("message", check=check)

    try:
        rolls, limit = map(int, msg.content.split(' '))
    except Exception:
        await ctx.send('형식에 맞춰서 입력해야지!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

# --- command for getting random inspired message ---


@bot.command()
async def inspire(ctx):
    quote = get_quote()
    await ctx.send(quote)


# --- command for taking a poll ---

@bot.command()
async def poll(ctx, *args):
    user_msg = ' '.join(args).strip()
    user_id = ctx.message.author.id
    if user_msg == '' or user_msg == None:
        await ctx.channel.purge(limit=1)
        await ctx.send(f'<@{user_id}> 주제를 입력해서 다시 시도해 줘!! ❌')
    else:
        await ctx.channel.purge(limit=1)
        await ctx.send(f'<@{user_id}> The poll has been accepted. ✅')
        embed = discord.Embed(title=':classical_building: Let\'s take a poll',
                              description=f'▸ {user_msg} \n\n 🔼 맘에 든다. · 🔽 맘에 들지 않는다.', color=0xdebce9)

        msg = await ctx.send(embed=embed)

        await msg.add_reaction('🔼')
        await msg.add_reaction('🔽')

# --- bot commands end --- #

nagative_things = ['슬프네']

positive_things = [
    '힘을 내!', '아니야 할 수 있어!', '기운을 내!', '기다려봐 좋은 일이 올거야!',
    '겨우 그거 가지고? 그건 아무것도 아니야!', '기운을 내!'
]

ends_msg = [
    '겠네', '겠네요', '겠군', '네요', '이겠군', '이군', '한듯', '인듯', '구나', '했네', '났네'
]

admiration_words = [
    '우와!', '정말?', '이야~', '워후~!', 'ㅎㅎ', 'thinking', '흠', 'ㅋㅋㅋ', '?', 'ㅇㅎ', 'ㄷㄷ'
]


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} !')

    # await bot.change_presence(activity = discord.Game(name=f"$Raon | $meme"))


@bot.listen('on_message')
async def whatever_user_typing(message):
    if message.author == bot.user:
        return

    if any(word in nagative_things for word in message.content.split(' ')):
        await message.channel.send(random.choice(positive_things))

    for word in message.content.split(' '):
        for ends_word in ends_msg:
            if word.endswith(ends_word):
                prob = random.randint(1, 10)
                if prob <= 7:
                    random_idx = random.randint(
                        0, custom_thinking_list.__len__() - 1)
                    await message.add_reaction(custom_thinking_list[random_idx])


@bot.event
async def on_member_join(member):

    # channel_id = 123456789

    e = discord.Embed(color=0xdebce9)
    e.set_image(url="https://static.wixstatic.com/media/6dcdca_ea9c49f57b4a4fa89cb2b51fb90d1c4a~mv2.jpg/v1/fill/w_1280,h_415,al_c,q_85/6dcdca_ea9c49f57b4a4fa89cb2b51fb90d1c4a~mv2.jpg")

    await bot.get_channel(channel_id).send(embed=e)

    embedVar = discord.Embed(
        title="Title goes here",
        description=f"Title description goes here",
        color=0xdebce9)

    embedVar.add_field(
        name="Title goes here",
        value="Paragraph goes here",
        inline=False)

    embedVar.add_field(name="Invite Link",
                       value="Actual link goes here",
                       inline=True)
    await bot.get_channel(channel_id).send(embed=embedVar)

    embed_rule = discord.Embed(
        title='Rule title goes here', color=0xdebce9)
    embed_rule.add_field(
        name='Title', value='Description', inline=False)

    await bot.get_channel(channel_id).send(embed=embed_rule)

keep_alive()
bot.run(os.getenv('TOKEN'))
