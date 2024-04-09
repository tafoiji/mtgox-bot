import requests
import BeautifulSoup
from random import randint
from time import sleep
from discord_webhook import DiscordWebhook
import discord
from discord.ext import commands
import asyncio
from private_settings import private_settings

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix='/', intents=intents)
run = True

url = 'https://www.mtgox.com'
token = private_settings.token
webhookLink = private_settings.webhookLink

def listOfLinks():
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    ListOfLinks = []
    p = soup.find('h3')
    # print(p)
    # print(p.find_all_next("a"))
    # print(soup.findAll("a"))
    for link in p.find_all_next("a"):
        lnk = link.get("href")

        if "http" not in lnk:
            urlNow = url + lnk
        else:
            urlNow = lnk
        if '.pdf' in urlNow and '_ja' not in urlNow and '_jp' not in urlNow:
            ListOfLinks.append(urlNow)
    return ListOfLinks


def webhookLinks(ListOfLinks):
    for urlNow in ListOfLinks:
        webhook = DiscordWebhook(username='mtgoxbot',
                                 url=webhookLink,
                                 rate_limit_retry=True, content=urlNow)
        webhook.execute()


def webhookFiles(ListOfLinks):
    for urlNow in ListOfLinks:
        webhook = DiscordWebhook(username='mtgoxbot',
                                 url=webhookLink,
                                 rate_limit_retry=True, content=urlNow)
        webhook.execute()
        webhook.content = ''
        pdf = requests.get(urlNow)
        webhook.add_file(file=pdf.content, filename=urlNow)
        webhook.execute()


def checkSite(finalListOfLinks, tempListOfLinks, s):
    index = len(tempListOfLinks) - len(finalListOfLinks)
    if index != 0:
        ListOfLinks = tempListOfLinks[:index]
        webhookTemp = DiscordWebhook(username='mtgoxbot',
                                     url=webhookLink,
                                     rate_limit_retry=True, content="NEW FILE(S) !!!!!!")
        webhookTemp.execute()
        if s == 'File':
            webhookFiles(ListOfLinks)
        else:
            webhookLinks(ListOfLinks)
    # else:
    #    webhook = DiscordWebhook(username='mtgoxbot',
    #                             url=webhookLink,
    #                             rate_limit_retry=True, content="NOTHING NEW")
    #    webhook.execute()


@client.command()
async def webhookAllLinks(message):
    ListOfLinks = listOfLinks()
    for urlNow in ListOfLinks:
        webhook = DiscordWebhook(username='mtgoxbot',
                                 url=webhookLink,
                                 rate_limit_retry=True, content=urlNow)

        webhook.execute()


@client.command()
async def webhookAllFiles(message):
    ListOfLinks = listOfLinks()
    for urlNow in ListOfLinks:
        webhook = DiscordWebhook(username='mtgoxbot',
                                 url=webhookLink,
                                 rate_limit_retry=True, content=urlNow)

        webhook.execute()
        webhook.content = ''
        pdf = requests.get(urlNow)
        webhook.add_file(file=pdf.content, filename=urlNow)
        webhook.execute()


@client.command()
async def stop(message):
    global run
    run = False


@client.command()
async def run_and_return_files(message):
    global run
    run = True
    finalListOfLinks = listOfLinks()
    while run:
        tempListOfLinks = listOfLinks()
        checkSite(finalListOfLinks, tempListOfLinks, 'File')
        finalListOfLinks.clear()
        finalListOfLinks = tempListOfLinks
        await asyncio.sleep(1)


@client.command()
async def run_and_return_links(message):
    global run
    run = True
    finalListOfLinks = listOfLinks()
    while run:
        tempListOfLinks = listOfLinks()
        checkSite(finalListOfLinks, tempListOfLinks, 'Links')
        finalListOfLinks.clear()
        finalListOfLinks = tempListOfLinks
        await asyncio.sleep(randint(55, 65))


client.run(token)
