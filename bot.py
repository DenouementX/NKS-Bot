# NKS-Bot: Battle Royale Stats Tracker
# Version: 1.0.0

import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
import requests
import matplotlib.pyplot as plt


#################################################################
####### using fortnitetracker's API to scrape player data #######
#################################################################

def seasonStats(name):
    # finds seasonal stats including wins, matches played, kd
    URL = 'https://api.fortnitetracker.com/v1/profile/pc/' + name
    headers = {'TRN-Api-Key' : 'ebfd96da-b6d3-4f00-9813-181297be2d49'}
    res = requests.get(URL, headers=headers)

    KDSolo = res.json()['stats']['curr_p2']['kd']['value']
    KDDuo = res.json()['stats']['curr_p10']['kd']['value']
    KDSquad = res.json()['stats']['curr_p9']['kd']['value']
    season_dict = ['Solo K/D', KDSolo, 'Duo K/D', KDDuo, 'Squad K/D', KDSquad]
    return (season_dict)

def lifeTimeStats(name):
    # finds lifetime stats including wins, matches played, kd
    URL = 'https://api.fortnitetracker.com/v1/profile/pc/' + name
    headers = {'TRN-Api-Key' : 'ebfd96da-b6d3-4f00-9813-181297be2d49'}
    res = requests.get(URL, headers=headers)
    lifeStats = res.json()['lifeTimeStats']
    
    lifetime_dict = {}
    for r in lifeStats:
        if r['key'] == 'Wins':
            lifetime_dict['Wins'] = r['value']
        if r['key'] == 'Matches Played':
            lifetime_dict['Matches Played'] = r['value']
        if r['key'] == 'K/d':
            lifetime_dict['K/D'] = r['value']
        if r['key'] == 'Win%':
            lifetime_dict['Win Rate'] = r['value']
    return lifetime_dict


#################################################################
############### maping player data in a pie chart ###############
#################################################################

def sgraph(name):
    # current season solo graph
    URL = 'https://api.fortnitetracker.com/v1/profile/pc/' + name
    headers = {'TRN-Api-Key' : 'ebfd96da-b6d3-4f00-9813-181297be2d49'}
    res = requests.get(URL, headers=headers)

    T1 = res.json()['stats']['curr_p2']['top1']['value']
    T10 = res.json()['stats']['curr_p2']['top10']['value']
    T25 = res.json()['stats']['curr_p2']['top25']['value']
    Total = res.json()['stats']['curr_p2']['matches']['value']
    Other = float(Total) - float(T1) - float(T10) - float(T25)

    labels = 'Top 1', 'Top 10', 'Top 25', 'Other'
    sizes = [T1, T10, T25, Other]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)  # explode 1st slice

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')

    # file1 = open('Picture.png', "w")
    # file1.write(plt.show())
    plt.savefig('stats.png')

def dgraph(name):
    # current season duo graph
    URL = 'https://api.fortnitetracker.com/v1/profile/pc/' + name
    headers = {'TRN-Api-Key' : 'ebfd96da-b6d3-4f00-9813-181297be2d49'}
    res = requests.get(URL, headers=headers)

    T1 = res.json()['stats']['curr_p10']['top1']['value']
    T5 = res.json()['stats']['curr_p10']['top5']['value']
    T12 = res.json()['stats']['curr_p10']['top12']['value']
    Total = res.json()['stats']['curr_p10']['matches']['value']
    Other = float(Total) - float(T1) - float(T5) - float(T12)

    labels = 'Top 1', 'Top 5', 'Top 12', 'Other'
    sizes = [T1, T5, T12, Other]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)  # explode 1st slice

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')

    # file1 = open('Picture.png', "w")
    # file1.write(plt.show())
    plt.savefig('stats.png')

def sqgraph(name):
    # current season squad graph
    URL = 'https://api.fortnitetracker.com/v1/profile/pc/' + name
    headers = {'TRN-Api-Key' : 'ebfd96da-b6d3-4f00-9813-181297be2d49'}
    res = requests.get(URL, headers=headers)

    T1 = res.json()['stats']['curr_p9']['top1']['value']
    T3 = res.json()['stats']['curr_p9']['top3']['value']
    T6 = res.json()['stats']['curr_p9']['top6']['value']
    Total = res.json()['stats']['curr_p9']['matches']['value']
    Other = float(Total) - float(T1) - float(T3) - float(T6)

    labels = 'Top 1', 'Top 3', 'Top 6', 'Other'
    sizes = [T1, T3, T6, Other]
    colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0, 0)  # explode 1st slice

    # Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    
    plt.axis('equal')

    # file1 = open('Picture.png', "w")
    # file1.write(plt.show())
    plt.savefig('stats.png')


#################################################################
##################### discord functionality #####################
#################################################################

Client = discord.Client() # Initialize Client 
client = commands.Bot(command_prefix = "?") # Initialize client bot

@client.event 
async def on_ready():
    print("Bot is online and connected to Discord.") # This will be called when the bot connects to the server

    # Bot status
    await client.change_presence(game=discord.Game(name='Type !HELP for list of commands.'))

@client.event
async def on_message(message):
    # Responds with functionality list
    if message.content.upper().startswith('!HELP'):
        await client.send_message(message.channel, "NKS-Bot: Battle Royale Stats Bot\n\n!COOKIE for a cookie emoji\n!PING for a PONG! response\n!SAY + words for a response with the words\n!SSTATS + name for seasonal stats\n!LSTATS + name for lifetime stats\n!SGRAPH + name for a graph of solo win %\n!DGRAPH + name for a graph of duo win %\n!SQGRAPH + name for a graph of squad win %")

    # Responds with Cookie emoji when someone says "cookie"
    if message.content.upper().startswith('!COOKIE'):
        await client.send_message(message.channel, ":cookie:")
   
    # Bot responds with Pong! and tags the user
    if message.content.upper().startswith('!PING'):
        userID = message.author.id
        await client.send_message(message.channel, "<@%s> PONG!" % (userID))
    
    # Bot replies with message you want it to say
    if message.content.upper().startswith('!SAY'):
        args = message.content.split(" ")
        await client.send_message(message.channel, "%s" % (" ".join(args[1:])))

    # Bot replies with seasonal stats
    if message.content.upper().startswith('!SSTATS'):
        args = message.content.split(" ")
        str1 = ' '.join(args[1:])
        await client.send_message(message.channel, seasonStats(str1))

    # Bot replies with lifetime stats
    if message.content.upper().startswith('!LSTATS'):
        args = message.content.split(" ")
        str1 = ' '.join(args[1:])
        await client.send_message(message.channel, lifeTimeStats(str1))
    
    # Bot replies with win % graph of current season solo
    if message.content.upper().startswith('!SGRAPH'):
        args = message.content.split(" ")
        str1 = ' '.join(args[1:])
        plt.gcf().clear()
        sgraph(str1)
        await client.send_file(message.channel, 'stats.png')

    # Bot replies with win % graph of current season duo
    if message.content.upper().startswith('!DGRAPH'):
        args = message.content.split(" ")
        str1 = ' '.join(args[1:])
        plt.gcf().clear()
        dgraph(str1)
        await client.send_file(message.channel, 'stats.png')

    # Bot replies with win % graph of current season squad
    if message.content.upper().startswith('!SQGRAPH'):
        args = message.content.split(" ")
        str1 = ' '.join(args[1:])
        plt.gcf().clear()
        sqgraph(str1)
        await client.send_file(message.channel, 'stats.png')

client.login(process.env.BOT_TOKEN)
