from cgitb import text
import os, discord, CUSTOMKIbot_functions as cst, random
from dotenv import load_dotenv
import shutil

from configparser import ConfigParser
from discord.ext import commands
from discord.utils import get
config = ConfigParser()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='C!', intents=intents)

textchannels = ('team1','team2','cards','customki-talks')
voicechannels = ('General','Team1', 'Team2')
role_names = ('CUSTOMKI_Team1','CUSTOMKI_Team2')

async def roles(ctx):
    created_roles = []
    for role_name in role_names:
        role = discord.utils.get(ctx.message.guild.roles, name=role_name)
        if role:
            try:
                await role.delete()
                print(f'{role} deleted.')
            except discord.Forbidden:
                print("Missing Permissions to delete this role!")
        else:
            print("The role doesn't exist!")
    
    for role in ctx.guild.roles:
        created_roles.append(role.name)
    for role in role_names:
        if role not in created_roles:
            await ctx.guild.create_role(name=role)
            print(f"Created '{role}' role")
    
    kategoria = get(ctx.guild.categories, name='CUSTOMKI')
    channels = tuple(get(kategoria.channels, name=n) for n in textchannels[0:2])
    roles_list = tuple(get(ctx.guild.roles, name=n) for n in role_names)

    for i in range(0, 2):
        await channels[i].set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False, view_channel=False)
        await channels[i].set_permissions(roles_list[i], read_messages=True, view_channel=True)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='setup',description='Setup CUSTOMKI!')
async def setup(ctx):
    
    category_names = []
    category_channels = []
    
    for cat in ctx.guild.categories:
        category_names.append(cat.name)
    if 'CUSTOMKI' not in category_names:
        await ctx.guild.create_category('CUSTOMKI')
        print("Category 'CUSTOMKI' has been created.")

    kategoria = get(ctx.guild.categories, name='CUSTOMKI')

    for channel in kategoria.channels:
        category_channels.append(channel.name)
    for channel in textchannels:
        if channel not in category_channels:
            await ctx.guild.create_text_channel(channel, category=kategoria)
    for channel in textchannels:
        if channel not in category_channels:
            await ctx.guild.create_text_channel(channel, category=kategoria)

    await ctx.send("Setup done!")
    
@bot.command(name='play',description='Just play CUSTOMKI. Remember to be connected to a voice channel with all the other players!')
async def play(ctx):
    await roles(ctx)
    
    voice_state = ctx.author.voice
    if voice_state is not None:
        channel = ctx.author.voice.channel
        memids = list(channel.voice_states.keys())
        if len(memids) != 10:
            await ctx.send(f"UWAGA! Aktualna liczba graczy: {len(memids)}. Sugerowana liczba graczy to: 10.")
        elif len(memids < 2):
            await ctx.send(f"UWAGA! Liczba graczy jest mniejsza niż: 2. Minimalna liczba graczy to: 2.")
            return()
        teamki = cst.losowanie_druzyn(memids)
        memuns = []

        for i in range (0,2):
            role = discord.utils.get(ctx.guild.roles, name=role_names[i])
            temp = []

            for id in teamki[i]:
                user = await bot.fetch_user(int(id))
                member = ctx.guild.get_member(int(id))
                await member.add_roles(role)
                temp.append(user.name)
            memuns.append(temp)

        print("The teams have been randomized.")
        print(f'TEAM 1: {memuns[0]}, TEAM 2: {memuns[1]}')

        embed=discord.Embed(title="CUSTOMKI - TEAMKI", color=0x883335)
        embed.set_thumbnail(url="https://i.imgur.com/JJA69Rn.png")
        embed.add_field(name="TEAM 1", value='\n'.join(memuns[0]), inline=True)
        embed.add_field(name="TEAM 2", value='\n'.join(memuns[1]), inline=True)
        await ctx.send(embed=embed)
        print('Embed sent.')

        kategoria = get(ctx.guild.categories, name='CUSTOMKI')
        channels = tuple(get(kategoria.channels, name=n) for n in textchannels[0:2])
        cst.rozdanie_kart()
        print("The cards have been drawn.")

        print("TEAM 1: " + str(cst.team1_cards))
        print("TEAM 2: " + str(cst.team2_cards))

        for i in range(0, 2):
            n = 0
            if i == 0:
                cards = cst.team1_cards
            elif i == 1:
                cards = cst.team2_cards
            filesToSend = [os.path.join(os.getcwd() + f'\\Team{i+1}\\',f) for f in os.listdir(os.getcwd() + f'\\Team{i+1}\\')]
            await channels[i].purge(limit=25)
            for f in filesToSend:
                await channels[i].send(file=discord.File(f),content=cards[n])
                n += 1
    else:
        await ctx.send("BŁĄD! - musisz być połączony z kanałem głosowym.")

@bot.command(name='handswap',description='Play the effect of the Hand Swap card! <caster_team> - number of team which played this card: <1>/<2>')
async def handswap(ctx, caster_team):
    cst.rozdaj('hand_swap', caster_team)
    print("'Hand Swap' has been played.")
    print("TEAM 1: " + str(cst.team1_cards))
    print("TEAM 2: " + str(cst.team2_cards))

    kategoria = get(ctx.guild.categories, name='CUSTOMKI')
    channels = tuple(get(kategoria.channels, name=n) for n in textchannels[0:2])
    filesToSend = [os.path.join(os.getcwd() + f'\\Team{caster_team}\\',f) for f in os.listdir(os.getcwd() + f'\\Team{caster_team}\\')]
    await channels[int(caster_team) - 1].purge(limit=25)
    await channels[int(caster_team) - 1].send('HAND SWAP:')
    if caster_team == '1':
        cards = cst.team1_cards
    elif caster_team == '2':
        cards = cst.team2_cards
    n = 0
    for f in filesToSend:
        await channels[int(caster_team) - 1].send(file=discord.File(f),content=cards[n])
        n += 1

@bot.command(name='infiltrator',description='Play the effect of the Infiltrator card! <caster_team> - number of team which played this card: <1>/<2>; [info] - list of cards IDs already played by that team, divided by commas: 23E,7C,2L')
async def infiltrator(ctx, caster_team, used=''):
    config.read('config.ini')
    kategoria = get(ctx.guild.categories, name='CUSTOMKI')
    channels = tuple(get(kategoria.channels, name=n) for n in textchannels[0:2])
    filesToRemove = [os.path.join(os.getcwd() + '\\CardEffects\\Infiltrator\\',k) for k in os.listdir(os.getcwd() + '\\CardEffects\\Infiltrator\\')]
    for k in filesToRemove:
        os.remove(k)
    if used == '':
            info = []
    else:
        info = used.split(',')
    n = int(config.get('main', 'ilosc_kart')) - len(info)
    if n > 3:
        n = 3
    if caster_team == '1':
        source = '\\Team2\\'
        for elem in info:
            cst.team2_cards.remove(elem)
        a = random.sample(cst.team2_cards, n)
    elif caster_team == '2':
        source = '\\Team1\\'
        for elem in info:
            cst.team1_cards.remove(elem)
        a = random.sample(cst.team1_cards, n)
    for card in a:
        shutil.copyfile(os.getcwd() + source + card + '.jpg', os.getcwd() + '\\CardEffects\\Infiltrator\\' + card + '.jpg')
        
    filesToSend = [os.path.join(os.getcwd() + '\\CardEffects\\Infiltrator\\',f) for f in os.listdir(os.getcwd() + '\\CardEffects\\Infiltrator\\')]
    await channels[int(caster_team) - 1].send('INFILTRATOR:')
    for f in filesToSend:
        await channels[int(caster_team) - 1].send(file=discord.File(f))

@bot.command(name='draw',description="Draw an additional card! <team> - number of team which wants to draw a card: <1>/<2>; [rarity] - rarity of the drawn card (leave empty if random): c/e/l")
async def draw(ctx, team, rarity=''):
    kategoria = get(ctx.guild.categories, name='CUSTOMKI')
    channels = tuple(get(kategoria.channels, name=n) for n in textchannels[0:2])
    card_details = cst.dobor_karty(rarity, team)
    card = os.getcwd() + f'\\CardBase\\{card_details[0]}\\'  + card_details[1] + '.jpg'
    await channels[int(team) - 1].send('DOBRANA KARTA:')
    await channels[int(team) - 1].send(file=discord.File(card),content=card_details[1])

@bot.command(name='ksero',description='Play the effect of the Ksero card! <caster_team> - number of team which played this card: <1>/<2>; [used] - list of cards IDs already played by that team, divided by commas: 23E,7C,2L')
async def ksero(ctx, caster_team, used=''):
    kategoria = get(ctx.guild.categories, name='CUSTOMKI')
    channels = tuple(get(kategoria.channels, name=n) for n in textchannels[0:2])
    if caster_team == '1':
        target = '2'
    elif caster_team == '2':
        target = '1'
    cardname = cst.ksero(target, used)
    card = os.getcwd() + f'\\Team{target}\\' + cardname + '.jpg'
    await channels[int(caster_team) - 1].send('SKSEROWANA KARTA:')
    await channels[int(caster_team) - 1].send(file=discord.File(card),content=cardname)
    print("A card has been photocopied.")

@bot.command(name='roll',description='Roll a dice! <max_value> - maximum value that can be rolled (minimum is: 1)')
async def roll(ctx, max_value=5):
    await ctx.send("Wylosowano liczbę: " + str(random.randint(1, int(max_value))))
bot.run(TOKEN)