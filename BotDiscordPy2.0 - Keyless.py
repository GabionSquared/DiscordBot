import discord
from discord.ext import commands
from discord.ui import Button, View

import random
import re       #(regex)
import gspread  #(for the spreadsheet)
import asyncio  #(for doing literally anything)
import datetime #(timers)
from datetime import date
from datetime import timedelta
import math     #(floating point)
from forex_python.converter import CurrencyRates

#region instantiation
CURRENCYRATES = CurrencyRates(force_decimal=False)

gc = gspread.service_account('client_secret.json')
sh = gc.open("Script Guild Spreadsheet")
WORKSHEET = sh.get_worksheet(0)

#THESE ARE FOR TWO DIFFERENT BOTS.
#use pen_nemisis while doing dev so you dont have to stop the main bot while you're doing it
DISCORD_TOKEN_PAL = "12345" #env is cringe
DISCORD_TOKEN_NEM = "12345"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="~", intents=intents)

#https://discordapp.com/oauth2/authorize?&client_id=682269398349774880&scope=bot

GUILDID = 1099437324703633521 #script haven
GUILD =  bot.get_guild(1099437324703633521)
PEOPLE = {}
CHANNELS = {}
CHANNELS_AUDIOS = {}
CHANNELS_SCRIPTS = {}
ROLES = {}
SOCIALCREDITCOUNTER = [[-1, -1]]
MONEYCOUNTER = [[-1, -1]]
BETTINGREWARD = 0.90

NEXTTICK = ""
MainUpdateTime = 60*60 #60 mins
#endregion

async def CollectObjects():
    global GUILD
    GUILD = bot.get_guild(1099437324703633521)
    global PEOPLE
    PEOPLE = {
    "Master"     : await bot.fetch_user(147745371303444480),
    "TestSubject": await bot.fetch_user(479068093902225411),
    "Echo"       : await bot.fetch_user(451263864051335169),
    "BlueChan"   : await bot.fetch_user(256502173788143626)
    }
    global CHANNELS
    CHANNELS = {
    "SelfRoles"     : bot.get_channel(1099438110594576486),
    "StarBoard"     : bot.get_channel(1099720977794994276),
    "General1"      : bot.get_channel(1099440036103077980),
    "General2"      : bot.get_channel(1099440038317658282),
    "Introductions" : bot.get_channel(1099495991780048978),
    "Furnace"       : bot.get_channel(1143327663130423317)
    }

    global CHANNELS_SCRIPTS
    CHANNELS_SCRIPTS = {
    "mystery-scripts"              : bot.get_channel(1099439300849975326),
    "humor-scripts"                : bot.get_channel(1099439649673449542),
    "drama-scripts"                : bot.get_channel(1099443467500916787),
    "romance-scripts"              : bot.get_channel(1099439060151439480),
    "monster-girl-boy-etc-scripts" : bot.get_channel(1099443678830919701),
    "experimental-scripts"         : bot.get_channel(1099443625533919332),
    "yandere-scripts"              : bot.get_channel(1099438971710349396),
    "action-scripts"               : bot.get_channel(1099464433018884106),
    "platonic-scripts"             : bot.get_channel(1099439034901741638),
    "adventure-scripts"            : bot.get_channel(1099439271108161677),
    "comfort-scripts"              : bot.get_channel(1099756541172785292),
    "tsundere-scripts"             : bot.get_channel(1099438995513016391),
    "horror-scripts"               : bot.get_channel(1099439708473405571),
    "slice-of-life-scripts"        : bot.get_channel(1099443532059644024),
    "fantasy-scifi-scripts"        : bot.get_channel(1099439319837581402)
    }

    global CHANNELS_AUDIOS
    CHANNELS_AUDIOS = {
    "horror-audios"               : bot.get_channel(1099443103083012117),
    "romance-audios"              : bot.get_channel(1099443203192651856),
    "tsundere-audios"             : bot.get_channel(1099443221534363668),
    "monster-girl-boy-etc-audios" : bot.get_channel(1099445002670706688),
    "experimental-audios"         : bot.get_channel(1099445568541032460),
    "yandere-audios"              : bot.get_channel(1099443238198325299),
    "drama-audios"                : bot.get_channel(1099445508709306378),
    "humor-audios"                : bot.get_channel(1099443123882557510),
    "platonic-audios"             : bot.get_channel(1099443177225732137),
    "mystery-audios"              : bot.get_channel(1099443145739096206),
    "adventure-audios"            : bot.get_channel(1099443056182317227),
    "comfort-audios"              : bot.get_channel(1099756604196409354),
    "action-audios"               : bot.get_channel(1099464362869133442),
    "slice-of-life-audios"        : bot.get_channel(1099445537645805578),
    "fantasy-scifi-audios"        : bot.get_channel(1099443082795167764),
    }

    global ROLES
    ROLES = {
    "R_Writer"   : discord.utils.get(GUILD.roles, id=1099446987557978122),
    "R_VA"       : discord.utils.get(GUILD.roles, id=1099447027357712384),
    "R_Editor"   : discord.utils.get(GUILD.roles, id=1099585107557371954),
    "R_Artist"   : discord.utils.get(GUILD.roles, id=1099584909389070406),
    "R_Listener" : discord.utils.get(GUILD.roles, id=1099455224353149089),

    "M_Open"  : discord.utils.get(GUILD.roles, id=1099447053614067804),
    "M_Close" : discord.utils.get(GUILD.roles, id=1099447118156017797),
    "M_Ask"   : discord.utils.get(GUILD.roles, id=1099447083649478887),

    "P_Him"   : discord.utils.get(GUILD.roles, id=1099705828145106965),
    "P_Her"   : discord.utils.get(GUILD.roles, id=1099705865629609994),
    "P_Them"  : discord.utils.get(GUILD.roles, id=1099705904775045271),
    "P_Other" : discord.utils.get(GUILD.roles, id=1099705935343124530),

    "E_Low"  : discord.utils.get(GUILD.roles, id=1099710261486702693),
    "E_Mid"  : discord.utils.get(GUILD.roles, id=1099710301911404585),
    "E_High" : discord.utils.get(GUILD.roles, id=1099710345645412422),

    "A_00-18" : discord.utils.get(GUILD.roles, id=1099705969866448936),
    "A_18-25" : discord.utils.get(GUILD.roles, id=1099706028590891098),
    "A_25-30" : discord.utils.get(GUILD.roles, id=1099706086426157056),
    "A_30-35" : discord.utils.get(GUILD.roles, id=1099706122983719043),
    "A_35-40" : discord.utils.get(GUILD.roles, id=1099706150464794744),
    "A_40-99" : discord.utils.get(GUILD.roles, id=1099706182467334274)
    }

    global COLOURROLES
    COLOURROLES = {
    1  : discord.utils.get(GUILD.roles, name="Writer's Pink"        +" (Colour)"),
    2  : discord.utils.get(GUILD.roles, name="Actor's Orange"       +" (Colour)"),
    3  : discord.utils.get(GUILD.roles, name="Editor's Blue"        +" (Colour)"),
    4  : discord.utils.get(GUILD.roles, name="Artist's Purple"      +" (Colour)"),
    5  : discord.utils.get(GUILD.roles, name="Listener's White"     +" (Colour)"),
    6  : discord.utils.get(GUILD.roles, name="Blue Violet"          +" (Colour)"),
    7  : discord.utils.get(GUILD.roles, name="City's Emerald"       +" (Colour)"),
    8  : discord.utils.get(GUILD.roles, name="Sludge Green"         +" (Colour)"),
    9  : discord.utils.get(GUILD.roles, name="Artificial Mint"      +" (Colour)"),
    10 : discord.utils.get(GUILD.roles, name="Dark And Stormy Night"+" (Colour)"),
    11 : discord.utils.get(GUILD.roles, name="Blue's Blue"          +" (Colour)"),
    12 : discord.utils.get(GUILD.roles, name="Deep Sea Blue"        +" (Colour)"),
    13 : discord.utils.get(GUILD.roles, name="Not Quite White"      +" (Colour)"),
    14 : discord.utils.get(GUILD.roles, name="Medium Rare"          +" (Colour)"),
    15 : discord.utils.get(GUILD.roles, name="Not Brown"            +" (Colour)"),
    16 : discord.utils.get(GUILD.roles, name="Bitter Tomato"        +" (Colour)"),
    17 : discord.utils.get(GUILD.roles, name="Banana Medicine"      +" (Colour)"),
    18 : discord.utils.get(GUILD.roles, name="Too Yellow"           +" (Colour)"),
    19 : discord.utils.get(GUILD.roles, name="Clown Pink"           +" (Colour)"),
    20 : discord.utils.get(GUILD.roles, name="Discord Background"   +" (Colour)"),
    }
 
SUPERSCRIPT_MAP = {
    "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶",
    "7": "⁷", "8": "⁸", "9": "⁹", "a": "ᵃ", "b": "ᵇ", "c": "ᶜ", "d": "ᵈ",
    "e": "ᵉ", "f": "ᶠ", "g": "ᵍ", "h": "ʰ", "i": "ᶦ", "j": "ʲ", "k": "ᵏ",
    "l": "ˡ", "m": "ᵐ", "n": "ⁿ", "o": "ᵒ", "p": "ᵖ", "q": "۹", "r": "ʳ",
    "s": "ˢ", "t": "ᵗ", "u": "ᵘ", "v": "ᵛ", "w": "ʷ", "x": "ˣ", "y": "ʸ",
    "z": "ᶻ", "A": "ᴬ", "B": "ᴮ", "C": "ᶜ", "D": "ᴰ", "E": "ᴱ", "F": "ᶠ",
    "G": "ᴳ", "H": "ᴴ", "I": "ᴵ", "J": "ᴶ", "K": "ᴷ", "L": "ᴸ", "M": "ᴹ",
    "N": "ᴺ", "O": "ᴼ", "P": "ᴾ", "Q": "Q", "R": "ᴿ", "S": "ˢ", "T": "ᵀ",
    "U": "ᵁ", "V": "ⱽ", "W": "ᵂ", "X": "ˣ", "Y": "ʸ", "Z": "ᶻ", "+": "⁺",
    "-": "⁻", "=": "⁼", "(": "⁽", ")": "⁾"}

ssm = str.maketrans(
    ''.join(SUPERSCRIPT_MAP.keys()),
    ''.join(SUPERSCRIPT_MAP.values()))
    #usage is "ass".translate(ssm) -> ᵃˢˢ

""" plan
1 self-assign roles
2 moderation help
3 random inspiration prompts on demand
4 autopost
6 birthday pings

Shit for the database idea:
    Able to subscribe into being availble for collabs by type
    (role?)
    "ask the bot to share a list of everyone who’s registered their interest in voicing a particular topic?"
    tracking active collabs
    "ask the bot about open collabs by theme."

sub milestones: 1k, 2.5k, 5k, 10k, then every 10k?
"""

@bot.event
async def on_ready():
    print(f"\033[33m\tLogged in as {bot.user}\033[0m")
    game = discord.Game("with the API")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    await CollectObjects()

    #for manually setting bits when things go wrong
    """    
    global SOCIALCREDITCOUNTER
    SOCIALCREDITCOUNTER = 
    
    #for i in range(1, len(SOCIALCREDITCOUNTER)):
    #    SOCIALCREDITCOUNTER[i][1] = SOCIALCREDITCOUNTER[i][1] * -1

    global MONEYCOUNTER
    MONEYCOUNTER = 
    """

    

    bot.loop.create_task(UpdateClockMain())

async def UpdateClockMain():
    while True:
        global NEXTTICK
        NEXTTICK = datetime.datetime.now() + datetime.timedelta(seconds=MainUpdateTime)
        print("\033[31mNEXT MAIN CLOCK:\033[0m")

        await Literally1985()
        UpdateServerSocialCredit()

        await asyncio.sleep(MainUpdateTime)

@bot.command(name = "socialcredit", help = "dolla dolla dolla")
async def PrintUserMoney(ctx):

    print("\033[33m\tCredit Check:\033[0m")
    userID = ctx.author.id

    result = usermoney(userID)
    if result == "???":
        await ctx.message.reply(f"nope. sorry, nothing.")
    else:
        await ctx.message.reply(f"You have " + str(result)+ " social credit!")


    print(f"\033[33m\tDone\033[0m")

@bot.command(name = "rank", help = "view your level, and how far you are to the next one!")
async def PrintUserRank(ctx):

    print("\033[33m\tCredit Check:\033[0m")
    userID = ctx.author.id

    result = usersocialcredit(userID)

    if result == "???":
        await ctx.message.reply(f"nope. sorry, nothing.")
    else:
        #leveling function
        truelevel = (-1 + math.sqrt(1 + 8 * result)) / 2
        level = math.floor(truelevel)
        percent = round((truelevel - level)*100, 1)

        await ctx.message.reply(f"you are level " + str(level) + "! (" + str(percent) + "%)")

    print(f"\033[33m\tDone\033[0m")

def usersocialcredit(userID):
    print("\033[33m\tSecret Credit Check:\033[0m")

    spot = None
    for i in range(len(SOCIALCREDITCOUNTER)):
            if SOCIALCREDITCOUNTER[i][0] == userID: 
                spot = i
                print(f"\033[33m\tIndex {i} in Live List\033[0m")

    try:
        cell = WORKSHEET.find(str(userID))
        socialCredit = int(WORKSHEET.cell(cell.row, 4).value)
        print(f"\033[33m\t[{socialCredit}] Stored Credit\033[0m")

        if spot != None:
            socialCredit = SOCIALCREDITCOUNTER[spot][1] + socialCredit
            print(f"\033[33m\t[{socialCredit}] Credit Adjusted\033[0m")

        return socialCredit

    except:
        print(f"\033[33m\tAn Error Occured (Not on the sheet?)\033[0m")
        return "???"

def usermoney(userID):
    print("\033[33m\tSecret Money Check:\033[0m")

    spot1 = None
    spot2 = None
    for i in range(len(SOCIALCREDITCOUNTER)):
            if SOCIALCREDITCOUNTER[i][0] == userID: 
                spot1 = i
                print(f"\033[33m\tIndex {i} in Live List\033[0m")

    for i in range(len(MONEYCOUNTER)):
            if MONEYCOUNTER[i][0] == userID: 
                spot2 = i
                print(f"\033[33m\tIndex {i} in Live Money List\033[0m")

    try:
        cell = WORKSHEET.find(str(userID))
        money = int(WORKSHEET.cell(cell.row, 14).value)
        print(f"\033[33m\t[{money}] Stored Credit\033[0m")

        if spot1 != None:
            money = SOCIALCREDITCOUNTER[spot1][1] + money
            print(f"\033[33m\t[{money}] Credit Adjusted (Social)\033[0m")
        
        if spot2 != None:
            money = MONEYCOUNTER[spot2][1] + money
            print(f"\033[33m\t[{money}] Credit Adjusted (Transaction)\033[0m")

        return int(money)

    except:
        return "???"

@bot.command(name = "leaderboard", help = "See the highest ranks on the server, and how you stack up!")
async def PrintUserSocialCreditLeaderboard(ctx, length: int = 3):
    print("\033[33m\tLeaderboard:\033[0m")

    userID = ctx.author.id
    if length > 10:
        length = 10
    if length < 3:
        length = 3

    ID_values_str = WORKSHEET.col_values("1")
    SC_values_str = WORKSHEET.col_values("4")
    outputString = ""

    All_SC_values = [int(x) for x in SC_values_str[1:]] #str -> int and trim title
    All_ID_values = [int(x) for x in ID_values_str[1:]] #str -> int and trim title

    for i in range(1, len(SOCIALCREDITCOUNTER)):
        try:
            index = All_ID_values.index(SOCIALCREDITCOUNTER[i][0])
            All_SC_values[index] = SOCIALCREDITCOUNTER[i][1] + All_SC_values[index]
        except:
            print(f"\033[33m{str(SOCIALCREDITCOUNTER[i][0])} is probably not in the server.\033[0m")

            continue


    #thanks chatgpt (sortin shit)
    sorted_indices = sorted(range(len(All_SC_values)), key=lambda i: All_SC_values[i], reverse=True)

    #user-specific bits
    CreditSpot = All_SC_values.index(usersocialcredit(ctx.author.id))
    CallerRank = sorted_indices.index(CreditSpot)+1
    print(f"\033[33m\tCaller is Rank {CallerRank}\n\033[0m")

    outputString += (f"you are rank " + str(CallerRank) + "!\n----------\n")

    def levelCheck(userID, credit):

        spot = None
        for i in range(len(SOCIALCREDITCOUNTER)):
                if SOCIALCREDITCOUNTER[i][0] == userID: 
                    spot = i
                    print(f"\033[33m\t\tIndex {i} in Live List\033[0m")

        if spot != None:
            credit = SOCIALCREDITCOUNTER[spot][1] + credit
            print(f"\033[33m\t\t[{credit}] Credit Adjusted\033[0m")

        level = math.floor((-1 + math.sqrt(1 + 8 * credit)) / 2) 
        return level

    for i in range (1, length+1): #the first one is the title
        row = sorted_indices[i-1]+2 #i have genuinly no idea why it needs an offset of 2. 1 indexed + title?

        cell_values = WORKSHEET.row_values(row)[0:4]
        #['944670449588133950', 'behawth', 'PositiviBee']

        print(f"\033[33m\t {i} : {cell_values}\033[0m")


        name = cell_values[2]
        if name == '':
            name = cell_values[1]
        
        outputString += ("Rank " + str(i) + ": " + name + ", level " + str(levelCheck(int(cell_values[0]),int(cell_values[3]))) + "\n")

    await ctx.message.reply(outputString)        

@bot.command(name = "smallify", help = "makes your message real small!")
async def smallify(ctx, message):
    print("\033[33m\tSmallify:\033[0m")
    string =  message.translate(ssm)
    await ctx.message.delete()
    await ctx.send(string)

@bot.command(name = "convert", help = "Quick Currency Conversions. Use like `~convert 10 GBP USD`or `~convert 10 GBP USD`")
async def convert(ctx, param1, param2, param3 = ""):
    #"~convert 10 GBP USD" and "~convert GBP USD"
    #one may observe that the optional param is in the middle
    print("\033[33m\tCurrency Conversion:\033[0m")

    conversionDate = date.today()#- timedelta(days = 1)

    if(param3 != ""):
        rate = CURRENCYRATES.convert(param2.upper(), param3.upper(), float(param1), conversionDate)
        rate = round(rate, 2)

        await ctx.message.reply(param1 + " " + param2.upper() + " -> " + str(rate) + " " + param3.upper())
        

    else:  #['~convert', 'GBP', 'USD']
        rate = CURRENCYRATES.convert(param1.upper(), param2.upper(), 1, conversionDate)
        rate = round(rate, 2)

        await ctx.message.reply("1 " + param1.upper() + " -> " + str(rate) + " " + param2.upper())

@bot.command(name = "roles", help = "Set yourself as a Writer, VA, Listener and more!")
async def create_button_roles(ctx):

    print("\033[33m\tRole Change:\033[0m")

    deleteTimer = 1

    button1_vaaaaa = Button(style=discord.ButtonStyle.blurple, label=f"VA 🎙️",       custom_id="vaaaaa")
    button2_writer = Button(style=discord.ButtonStyle.blurple, label=f"Writer ✍️",   custom_id="writer")
    button3_editor = Button(style=discord.ButtonStyle.blurple, label=f"Editor 💻",   custom_id="editor")
    button4_artist = Button(style=discord.ButtonStyle.blurple, label=f"Artist 🎨",   custom_id="artist")
    button5_listen = Button(style=discord.ButtonStyle.blurple, label=f"Listener 🎧", custom_id="listen")

    async def button_vaaaaa(interaction: discord.Interaction):
        if ROLES["R_VA"] in interaction.user.roles:
            await interaction.user.remove_roles(ROLES["R_VA"])
            await interaction.response.send_message("Removed VA Role", delete_after = deleteTimer)
            print(f"\033[33m\nRemoved [R_VA] From {interaction.user.nick}\033[0m")

        else:
            await interaction.user.add_roles(ROLES["R_VA"])
            await interaction.response.send_message("Added VA Role", delete_after = deleteTimer)
            print(f"\033[33m\nAdded [R_VA] From {interaction.user.nick}\033[0m")


    async def button_writer(interaction: discord.Interaction):
        if ROLES["R_Writer"] in interaction.user.roles:
            await interaction.user.remove_roles(ROLES["R_Writer"])
            await interaction.response.send_message("Removed Writer Role", delete_after = deleteTimer)
            print(f"\033[33m\nRemoved [R_Writer] From {interaction.user.nick}\033[0m")
        else:
            await interaction.user.add_roles(ROLES["R_Writer"])
            await interaction.response.send_message("Added Writer Role", delete_after = deleteTimer)
            print(f"\033[33m\nAdded [R_Writer] From {interaction.user.nick}\033[0m")
    
    async def button_editor(interaction: discord.Interaction):
        if ROLES["R_Editor"] in interaction.user.roles:
            await interaction.user.remove_roles(ROLES["R_Editor"])
            await interaction.response.send_message("Removed Editor Role", delete_after = deleteTimer)
            print(f"\033[33m\nRemoved [R_Editor] From {interaction.user.nick}\033[0m")
        else:
            await interaction.user.add_roles(ROLES["R_Editor"])
            await interaction.response.send_message("Added Editor Role", delete_after = deleteTimer)
            print(f"\033[33m\nAdded [R_Editor] From {interaction.user.nick}\033[0m")

    async def button_artist(interaction: discord.Interaction):
        if ROLES["R_Artist"] in interaction.user.roles:
            await interaction.user.remove_roles(ROLES["R_Artist"])
            await interaction.response.send_message("Removed Artist Role", delete_after = deleteTimer)
            print(f"\033[33m\nRemoved [R_Artist] From {interaction.user.nick}\033[0m")
        else:
            await interaction.user.add_roles(ROLES["R_Artist"])
            await interaction.response.send_message("Added Artist Role", delete_after = deleteTimer)
            print(f"\033[33m\nAdded [R_Artist] From {interaction.user.nick}\033[0m")
    
    async def button_listen(interaction: discord.Interaction):
        if ROLES["R_Listener"] in interaction.user.roles:
            await interaction.user.remove_roles(ROLES["R_Listener"])
            await interaction.response.send_message("Removed Listener Role", delete_after = deleteTimer)
            print(f"\033[33m\nRemoved [R_Listener] From {interaction.user.nick}\033[0m")
        else:
            await interaction.user.add_roles(ROLES["R_Listener"])
            await interaction.response.send_message("Added Listener Role", delete_after = deleteTimer)
            print(f"\033[33m\nAdded [R_Listener] From {interaction.user.nick}\033[0m")

    view = View()
    view.add_item(button1_vaaaaa)
    view.add_item(button2_writer)
    view.add_item(button3_editor)
    view.add_item(button4_artist)
    view.add_item(button5_listen)
    view.timeout = None

    await ctx.send("Give yourself some roles!\n(Clicking one you already have will remove it)", view=view)

    bot.add_view(view)
    button1_vaaaaa.callback = button_vaaaaa
    button2_writer.callback = button_writer
    button3_editor.callback = button_editor
    button4_artist.callback = button_artist
    button5_listen.callback = button_listen

#region the great reacting

@bot.command(name = "reactttttttt", hidden=True)
async def react(ctx):
    print("\033[33m\treactttttttt (Add Reactions To All Posts):\033[0m")

    pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"

    #async for message in ctx.channel.history(limit=None):
    #    if(re.search(pattern, message.content)):
    #        await message.add_reaction("\u2B50")
    #

    for channel in CHANNELS_AUDIOS.values():
        print(channel.name)
        print(f"\033[33m\t{channel.name}\033[0m")
        async for message in channel.history(limit=None):
            if(re.search(pattern, message.content)):
                await message.add_reaction("\u2B50")

    for channel in CHANNELS_SCRIPTS.values():
        print(f"\033[33m\t{channel.name}\033[0m")
        async for message in channel.history(limit=None):
            if(re.search(pattern, message.content)):
                await message.add_reaction("\u2B50")

    print(f"\033[33m\tdone\033[0m")

@bot.command(name = "unreactttttttt", hidden=True)
async def unreact(ctx):
    print("\033[33\tmunreactttttttt (Remove Reactions To All Posts):\033[0m")

    for channel in CHANNELS_AUDIOS.values():
        print(f"\033[33m\t{channel.name}\033[0m")
        async for message in channel.history(limit=None):
            reaction = discord.utils.get(message.reactions, emoji="\u2B50")
            if reaction:
                await reaction.remove(bot.user)

    for channel in CHANNELS_SCRIPTS.values():
        print(f"\033[33m\t{channel.name}\033[0m")
        async for message in channel.history(limit=None):
            reaction = discord.utils.get(message.reactions, emoji="\u2B50")
            if reaction:
                await reaction.remove(bot.user)

    print(f"\033[33m\tdone\033[0m")

@bot.command(name = "reactSpecific", hidden=True)
async def reactSpecific(ctx, channelid, messageid):
    print("\033[33m\treactSpecific:\033[0m")

    channel = bot.get_channel(channelid)
    message = await channel.get_message(messageid)

    await message.add_reaction("\u2B50")

#endregion

#region colours
async def RemoveColourRole(interaction: discord.Interaction):
    print("\033[33m\tRemoveColourRole:\033[0m")
    
    for role in COLOURROLES.values():
        if(role in interaction.user.roles):
            await interaction.user.remove_roles(role)
            print(f"\033[33m\tRemoved {role.name} From {interaction.user.nick}\033[0m")
    
    # it would probably be faster to index user roles like this, but it just
    # says "KeyError: 0" and im too tired to figure out what that means
    """
    for i in range (len(interaction.user.roles)):
        if(COLOURROLES[i] in interaction.user.roles):
            await interaction.user.remove_roles(COLOURROLES[i])
    """
    
@bot.command(name = "colours", aliases=['colors','colour', 'color'], help = "Get yourself a colourful name!")
async def create_button_colours(ctx):
    print(f"\033[33m\tCreating Colour Menu:\033[0m")

    deleteTimer = 1

    button1 = Button(style=discord.ButtonStyle.blurple, label=f"1", custom_id="c1")
    button2 = Button(style=discord.ButtonStyle.blurple, label=f"2", custom_id="c2")
    button3 = Button(style=discord.ButtonStyle.blurple, label=f"3", custom_id="c3")
    button4 = Button(style=discord.ButtonStyle.blurple, label=f"4", custom_id="c4")
    button5 = Button(style=discord.ButtonStyle.blurple, label=f"5", custom_id="c5")
    button6 = Button(style=discord.ButtonStyle.blurple, label=f"6", custom_id="c6")
    button7 = Button(style=discord.ButtonStyle.blurple, label=f"7", custom_id="c7")
    button8 = Button(style=discord.ButtonStyle.blurple, label=f"8", custom_id="c8")
    button9 = Button(style=discord.ButtonStyle.blurple, label=f"9", custom_id="c9")
    button10 = Button(style=discord.ButtonStyle.blurple, label=f"10", custom_id="c10")
    button11 = Button(style=discord.ButtonStyle.blurple, label=f"11", custom_id="c11")
    button12 = Button(style=discord.ButtonStyle.blurple, label=f"12", custom_id="c12")
    button13 = Button(style=discord.ButtonStyle.blurple, label=f"13", custom_id="c13")
    button14 = Button(style=discord.ButtonStyle.blurple, label=f"14", custom_id="c14")
    button15 = Button(style=discord.ButtonStyle.blurple, label=f"15", custom_id="c15")
    button16 = Button(style=discord.ButtonStyle.blurple, label=f"16", custom_id="c16")
    button17 = Button(style=discord.ButtonStyle.blurple, label=f"17", custom_id="c17")
    button18 = Button(style=discord.ButtonStyle.blurple, label=f"18", custom_id="c18")
    button19 = Button(style=discord.ButtonStyle.blurple, label=f"19", custom_id="c19")
    button20 = Button(style=discord.ButtonStyle.blurple, label=f"20", custom_id="c20")

    """
    in theory you could change this to something like

    async def Callback(rolenumber, interaction: discord.interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[rolenumber])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)

    but i dont know enough about callback params
    """

    async def Cbutton1(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[1])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[1].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton2(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[2])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[2].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton3(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[3])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[3].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton4(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[4])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[4].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton5(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[5])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[5].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton6(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[6])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[6].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton7(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[7])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[7].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton8(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[8])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[8].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton9(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[9])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[9].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton10(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[10])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[10].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton11(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[11])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[11].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton12(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[12])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[12].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton13(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[13])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[13].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton14(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[14])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[14].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton15(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[15])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[15].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton16(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[16])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[16].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton17(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[17])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[17].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton18(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[18])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[18].name} To {interaction.user.nick}\033[0m")
    
    async def Cbutton19(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[19])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[19].name} To {interaction.user.nick}\033[0m")

    async def Cbutton20(interaction: discord.Interaction):
        await RemoveColourRole(interaction)
        await interaction.user.add_roles(COLOURROLES[20])
        await interaction.response.send_message("Changed Colour", delete_after = deleteTimer)
        print(f"\033[33m\tAdded {COLOURROLES[20].name} To {interaction.user.nick}\033[0m")

    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    view.add_item(button4)
    view.add_item(button5)
    view.add_item(button6)
    view.add_item(button7)
    view.add_item(button8)
    view.add_item(button9)
    view.add_item(button10)
    view.add_item(button11)
    view.add_item(button12)
    view.add_item(button13)
    view.add_item(button14)
    view.add_item(button15)
    view.add_item(button16)
    view.add_item(button17)
    view.add_item(button18)
    view.add_item(button19)
    view.add_item(button20)
    view.timeout = None


    with open("Colours.png", "rb") as file:
        await ctx.send("Feeling a little colourful?~", view=view, file=discord.File(file))

    bot.add_view(view)
    button1.callback = Cbutton1
    button2.callback = Cbutton2
    button3.callback = Cbutton3
    button4.callback = Cbutton4
    button5.callback = Cbutton5
    button6.callback = Cbutton6
    button7.callback = Cbutton7
    button8.callback = Cbutton8
    button9.callback = Cbutton9
    button10.callback = Cbutton10
    button11.callback = Cbutton11
    button12.callback = Cbutton12
    button13.callback = Cbutton13
    button14.callback = Cbutton14
    button15.callback = Cbutton15
    button16.callback = Cbutton16
    button17.callback = Cbutton17
    button18.callback = Cbutton18
    button19.callback = Cbutton19
    button20.callback = Cbutton20

@bot.command(name = "randomise", aliases=['randomize'], help = "if ~colours is too many choises for you")
async def RandomiseColour(ctx):
    print(f"\033[33m\tRandomise Colour\033[0m")

    for role in COLOURROLES.values():
        if(role in ctx.author.roles):
            await ctx.author.remove_roles(role)
    role = COLOURROLES[random.randint(1, 20)]

    await ctx.author.add_roles(role)

    await ctx.message.reply("You rolled " + role.name[:-9] + "!")
    print(f"\033[33m\tAdded {role.name} To {ctx.author.nick}\033[0m")
#endregion

@bot.event
async def on_message(message): #this should be ONLY the "every message" shit
    #social credit counting
    credit = UpdateLocalSocialCredit(message.author.id)
    if(not message.author.nick == None):
        name = message.author.nick
    else:
        name = message.author.name

    print(f"\033[34m{name}: \033[0m{str(credit)}\033[32m {message.content.lower()}\033[0m")

    #this is down here so PenPal can get social credit like the good boy he is. he IS in the sheet.
    if message.author == bot.user:
        return

    #region reacting
    if(message.channel in CHANNELS_SCRIPTS.values() or message.channel in CHANNELS_AUDIOS.values()):
        pattern = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+" #has a url
        if(re.search(pattern, message.content)):
            await message.add_reaction("\u2B50")
            print(f"\033[33m\tAdded Star Reaction\033[0m")


    if(message.channel == CHANNELS["Furnace"] and message.author != 682269398349774880): #the bot, so it doesnt delete the furnace image
        await F_begin()
        print(f"\033[33m\tFurnace Triggered\033[0m")
    #endregion

    #region parrot
    txt = message.content.lower()

    if txt.startswith('ping'):
        print("\033[33m\tPing:\033[0m")
        await message.channel.send("pong")

    if txt.startswith('pong'):
        print("\033[33m\tPing:\033[0m")
        await message.channel.send("ping")
        
    if txt.startswith('marco'):
        print("\033[33m\tPing:\033[0m")
        await message.channel.send("polo")
        
    if txt.startswith('polo'):
        print("\033[33m\tPing:\033[0m")
        await message.channel.send("marco")
        
    if txt.startswith('sweet caroline'):
        print("\033[33m\tPing:\033[0m")
        await message.channel.send("BUM BUM BUM")

    if txt.startswith('good times never seemed so good'):
        print("\033[33m\tPing:\033[0m")
        await message.channel.send("SO GOOD! SO GOOD!")

    if txt.startswith('le ping'):
        print("\033[33m\tPing:\033[0m")
        await message.channel.send("le pong")
    
    if txt.startswith('le pong'):
        print("\033[33m\tPing:\033[0m")
        await message.channel.send("le ping")
    #endregion

    await bot.process_commands(message)

#region Social Credit Management
def UpdateLocalSocialCredit(userID):
    global SOCIALCREDITCOUNTER

    spot = None
    for i in range(len(SOCIALCREDITCOUNTER)):
            if SOCIALCREDITCOUNTER[i][0] == userID: 
                spot = i

    if spot == None:
        print("\033[33mNew User Speaks:\033[0m")
        SOCIALCREDITCOUNTER.append([userID, 1])
        print(SOCIALCREDITCOUNTER)
        print("\033[31m" + str(NEXTTICK) + "\033[0m")
        return 1

    else:
        temp = SOCIALCREDITCOUNTER[spot][1]
        temp += 1
        SOCIALCREDITCOUNTER[spot][1] = temp
        print(SOCIALCREDITCOUNTER)
        print("\033[31m" + str(NEXTTICK) + "\033[0m")
        return SOCIALCREDITCOUNTER[spot][1]

@bot.command(name = "forcesync", hidden=True)
async def ForceUpdateServerSocialCredit(ctx):
    if ctx.author.id !=  147745371303444480:
        return
    UpdateServerSocialCredit()

def UpdateServerSocialCredit():
    print(f"\033[33m\tUpdateServerSocialCredit\033[0m")

    Sheet_ID_values = WORKSHEET.col_values("1")
    Sheet_MessageCount_values = WORKSHEET.col_values("4")
    Sheet_Currency_values = WORKSHEET.col_values("14")
    global SOCIALCREDITCOUNTER
    global MONEYCOUNTER

    #iterate the messages list
    for i in range(1, len(SOCIALCREDITCOUNTER)):
        try:
            spot = Sheet_ID_values.index(str(SOCIALCREDITCOUNTER[i][0]))
        except:
            print(f"\033[33m{str(SOCIALCREDITCOUNTER[i][0])} is probably not in the server.\033[0m")

            continue
        
        #adds the message counter values to whats going to be pasted on the sheet
        Sheet_MessageCount_values[spot] = int(Sheet_MessageCount_values[spot]) + SOCIALCREDITCOUNTER[i][1]

        Sheet_Currency_values[spot] = int(Sheet_Currency_values[spot]) + SOCIALCREDITCOUNTER[i][1]


    #iterate the money list
    for i in range(1, len(MONEYCOUNTER)):
        try:
            spot = Sheet_ID_values.index(str(MONEYCOUNTER[i][0]))
        except:
            print(f"\033[33m{str(MONEYCOUNTER[i][0])} is probably not in the server.\033[0m")

            continue
        
        #adds the message counter values to whats going to be pasted on the sheet
        Sheet_Currency_values[spot] = int(Sheet_Currency_values[spot]) + MONEYCOUNTER[i][1]

    #this now needs 2 calls because idk how to make it take 1 again
    range_label = f'D1:D{len(Sheet_MessageCount_values)+1}'
    cell_list = WORKSHEET.range(range_label)

    for i in range(len(Sheet_MessageCount_values)):
        cell_list[i].value = Sheet_MessageCount_values[i]
    WORKSHEET.update_cells(cell_list)


    range_label = f'N1:N{len(Sheet_Currency_values)+1}'
    cell_list = WORKSHEET.range(range_label)

    for i in range(len(Sheet_Currency_values)):
        cell_list[i].value = Sheet_Currency_values[i]
    WORKSHEET.update_cells(cell_list)

    SOCIALCREDITCOUNTER = [[-1, -1]]
    MONEYCOUNTER = [[-1, -1]]
#endregion

#region server scraping bits
async def Literally1985(): #rework of the old command, which was actually called 1984 
    print(f"\033[33m\tLiterally1985\033[0m")

    users = GUILD.members
    data = WORKSHEET.get_all_values()

    async for last_message in CHANNELS["Introductions"].history(limit=1):
        break
    introMessages = CHANNELS["Introductions"].history(before=last_message, oldest_first=False)

    #process intromessages into an id:messageContent dict?

    print(f"\033[33m\tServer Pop: [{len(users)}]\n\033[0m")

    for i in range(0, len(users)):
        row = None
        user = users[i]
        print(f"\033[33m\t({str(i)}) : {user.name}\033[0m")
        id = str(user.id)

        #getting what row that user's on
        for i in range(1, len(data)): #skipping data[0][0] "ID"
            checkid = data[i][0]
            if (checkid == id): 
                row = i

        #user dont exist
        if row == None:
            print(f"\033[33m\t\tNew User Found: {user.name}\033[0m")
            data.append(await GetUserProfile(user, introMessages))
            continue
        
        #checking nicknames
        data[row][1] = user.name
        if(not user.nick == None):
            data[row][2] = user.nick
        else:
            data[row][2] = ''
        
        #dont touch social credits

        #check roles
        if len(user.roles) == 1: #only role is @everyone, user's a whitename.
            data[row][4] = "TRUE"
            data[row][5] = "FALSE"
            data[row][6] = "FALSE"
            data[row][7] = "FALSE"
            data[row][8] = "FALSE"
            data[row][9] = "FALSE"
        else:
            data[row][4] = "FALSE"
            data[row][5] = "TRUE" if ROLES["R_VA"] in user.roles else "FALSE"
            data[row][6] = "TRUE" if ROLES["R_Writer"] in user.roles else "FALSE"
            data[row][7] = "TRUE" if ROLES["R_Editor"] in user.roles else "FALSE"
            data[row][8] = "TRUE" if ROLES["R_Artist"] in user.roles else "FALSE"
            data[row][9] = "TRUE" if ROLES["R_Listener"] in user.roles else "FALSE"

        """
        #check youtube channel in intros
        if(data[row][10] == ''): #only really want to check if there isnt one already
            print("     checking for message")
            async for message in introMessages:
                if message.author == user:
                    print("     checking for link")
                    data[row][10] = await IfHasYouTubeLink(message.content)
                    break
        """
        #subs and shit

        #['147745371303444480', 'Spooks?', 'Ash Moth Audio', '701', 'FALSE', 'TRUE', 'FALSE', 'TRUE', 'FALSE', 'TRUE', 'https://www.youtube.com/@AshMothAudio', '0', '0'] 

    #now we have the "data" array that we need to just dump onto the sheet

    #TEST SHEET
    #sheet = sh.get_worksheet(1)

    rows = []
    for row in data:
        rows.append([str(cell) for cell in row])
    cell_range = f"A1:{chr(ord('A') + len(data[0]) - 1)}{len(data)}"
    WORKSHEET.update(cell_range, rows)


async def GetUserProfile(user, MessagesInIntros):
    youtube = ""
    socialCredit = 0
    money = 0

    nick = ''
    if(not user.nick == None):
            nick = user.nick

    #check if their #introductions message has a yt link in it
    async for message in MessagesInIntros:
        if message.author == user:
            youtube = await IfHasYouTubeLink(message.content)
            break

    whiteName = "FALSE"
    va = "FALSE"
    writer = "FALSE"
    editor = "FALSE"
    artist = "FALSE"
    listener = "FALSE"

    if len(user.roles) == 1: #@everyone
        whiteName = "TRUE"
    else:
        va =       "TRUE" if ROLES["R_VA"] in user.roles else "FALSE"
        writer =   "TRUE" if ROLES["R_Writer"] in user.roles else "FALSE"
        editor =   "TRUE" if ROLES["R_Editor"] in user.roles else "FALSE"
        artist =   "TRUE" if ROLES["R_Artist"] in user.roles else "FALSE"
        listener = "TRUE" if ROLES["R_Listener"] in user.roles else "FALSE"



    arr = [str(user.id), user.name, nick, socialCredit, whiteName, va, writer, editor, artist, listener, youtube, 0, 0, money]
    return arr

async def IfHasYouTubeLink(string): #todo make youtube api work
    print(string)
    youtube_regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:(?:watch\?v=([a-zA-Z0-9_-]{11}))|(?:channel\/([a-zA-Z0-9_-]{24}))|(?:@([a-zA-Z0-9_-]+)))"
    match = re.search(youtube_regex, string)
    print(match)
    if match:
        # check which part of the link was matched and construct the full YouTube link
        if match.group(1):
            # video link
            youtube_link = "https://www.youtube.com/watch?v=" + match.group(1)
        elif match.group(2):
            # channel link
            youtube_link = "https://www.youtube.com/channel/" + match.group(2)
        elif match.group(3):
            # user link
            youtube_link = "https://www.youtube.com/@" + match.group(3)
        return youtube_link
    else:
        return ""

#endregion

#region furnace

furnaceState = ""
deletionTime = 3
furnaceTime = 10

async def F_begin():
    await CHANNELS["Furnace"].send("🔥🔥🔥🔥")
    await asyncio.sleep(deletionTime)
    await F_light()

async def F_light():

    await CHANNELS["Furnace"].purge(limit=None)

    with open("Furnace_on.png", "rb") as file:
        await CHANNELS["Furnace"].send("", file=discord.File(file))
    
    await asyncio.sleep(furnaceTime)
    await F_unlight()

async def F_unlight():

    await CHANNELS["Furnace"].purge(limit=None)

    with open("Furnace_off.png", "rb") as file:
        await CHANNELS["Furnace"].send("", file=discord.File(file))

#endregion

#region gamba & monee
def CanUserAfford(userID, amount):
    held = usermoney(userID)

    if(held == "???"):
        print("read error occured")
        return

    if amount > held or amount < 0:
        print(f"\033[33m\nuser can't afford {amount} ({held-amount}) :\033[0m")
        return False
    else:
        print("\033[33m\nuser can afford\n\033[0m")
        return True


    AdjustUserMoney(ctx.author.id, -10)

def AdjustUserMoney(userID, amount):
    global MONEYCOUNTER
    print(MONEYCOUNTER)

    spot = None
    for i in range(len(MONEYCOUNTER)):
            if MONEYCOUNTER[i][0] == userID: 
                spot = i

    if spot == None:
        print("\033[33mNew User Transaction:\033[0m")
        MONEYCOUNTER.append([userID, amount])
        print(MONEYCOUNTER)
        print("\033[31m" + str(NEXTTICK) + "\033[0m")
        return 1

    else:
        temp = MONEYCOUNTER[spot][1]
        temp += amount
        MONEYCOUNTER[spot][1] = temp #it gets weird with just adding it straight in
        print(MONEYCOUNTER)
        print("\033[31m" + str(NEXTTICK) + "\033[0m")

@bot.command(name = "gift")
async def Gift(ctx, user: discord.Member, amount):
    amount = int(amount)

    if (not CanUserAfford(ctx.author.id, amount)):
        await ctx.message.reply("You can't afford that!")
        return
    
    _ = amount * -1
    AdjustUserMoney(ctx.author.id, _)

    AdjustUserMoney(user.id, amount)


@bot.command(name = "betflip", aliases=['bf'])
async def Flip(ctx, headsOrTails, betValue):
    userID = ctx.author.id
    
    heads = ["heads", "head", "h"]
    tails = ["tails", "tail", "t"]

    if(headsOrTails not in heads and headsOrTails not in tails):
        await ctx.message.reply("What side?\nEg '~betflip heads 100' or '~bf t 5'")
        return

    try:
        betValue = int(betValue)
    except:
        await ctx.message.reply("How much?\nEg '~betflip heads 100' or '~bf t 5'")
        return
    
    if (not CanUserAfford(userID, betValue)):
        await ctx.message.reply("You can't afford that!")
        return

    reward = math.floor(betValue*BETTINGREWARD)
    
    #0 is heads, 1 is tails
    WantHeads = 1 if headsOrTails in heads == None else 0
    roll = random.randint(0,1)
    userWin = roll == WantHeads
    print(f"\033[33m\tuser wants {'tails' if WantHeads == 1 else 'heads'}, rolled {'tails' if roll == 1 else 'heads'}\033[0m")
    print(f"\033[33m\tpaid {betValue}, reward is {reward} on {BETTINGREWARD} multiplier ({betValue+reward} pot)\033[0m")

    if(userWin):

        embed = discord.Embed(
            title="You guessed it! You won " + str(reward+betValue) + " credits!",
            #description="yeag", #non-bold text underneath
            color=ctx.author.colour #the strip down the side
        )
        name = ctx.author.name if ctx.author.nick == None else ctx.author.nick
        embed.set_author(name=name, icon_url=(ctx.author.display_avatar))

        if(roll == 0):
            file = discord.File("Coin_Heads.png", filename="Coin_Heads.png")
            embed.set_image(url="attachment://Coin_Heads.png")
        else:
            file = discord.File("Coin_Tails.png", filename="Coin_Tails.png")
            embed.set_image(url="attachment://Coin_Tails.png")

        await ctx.message.reply(file = file, embed=embed)

        AdjustUserMoney(userID, reward)
        AdjustUserMoney(682269398349774880, reward*-1) #the bot
    
    else: #user lost

        embed = discord.Embed(
            title="Better Luck Next time!",
            #description="yeag", #non-bold text underneath
            color=ctx.author.colour #the strip down the side
        )
        name = ctx.author.name if ctx.author.nick == None else ctx.author.nick
        embed.set_author(name=name, icon_url=(ctx.author.display_avatar))

        if(roll == 0):
            file = discord.File("Coin_Heads.png", filename="Coin_Heads.png")
            embed.set_image(url="attachment://Coin_Heads.png")
        else:
            file = discord.File("Coin_Tails.png", filename="Coin_Tails.png")
            embed.set_image(url="attachment://Coin_Tails.png")

        await ctx.message.reply(file = file, embed=embed)

        AdjustUserMoney(userID, betValue*-1)
        AdjustUserMoney(682269398349774880, betValue) #the bot



#endregion
bot.run(DISCORD_TOKEN_PAL) #env is still cringe