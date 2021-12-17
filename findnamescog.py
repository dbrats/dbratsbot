import requests
import psycopg2
import os
from dotenv import load_dotenv
from discord.ext import tasks

load_dotenv()
HOST = os.getenv('PG_HOST')
DATABASE = os.getenv('PG_DATABASE')
USER = os.getenv('PG_USER')
PASSWORD = os.getenv('PG_PASSWORD')

dbconn = psycopg2.connect(
    host=HOST,
    port=5432,
    database=DATABASE,
    user=USER,
    password=PASSWORD
)

friendNames = ["Theodor", "Thomas", "Marius", "Jørgen", "J%C3%B8rgen", "Ariel", "Jakob"]

friendNamesMap = {
    "Theodor" : "<@120114285845282817>",
    "Thomas" : "<@581885571396272173>",
    "Marius" : "<@604284074906877962>",
    "Jørgen" : "<@552440549265637378>",
    "J%C3%B8rgen" : "<@552440549265637378>",
    "Ariel" : "<@216119259003092995>",
    "Jakob" : "<@217676511296094209>"
}

friendYoutubeMap = {
    "Theodor" : "https://www.youtube.com/watch?v=qzEoBrr9gRA",
    "Thomas" : "https://www.youtube.com/watch?v=hSVFRyEYSLw",
    "Marius" : "https://www.youtube.com/watch?v=ehSRzM2DN2k",
    "Jørgen" : "https://www.youtube.com/watch?v=gxEPV4kolz0",
    "J%C3%B8rgen" : "https://www.youtube.com/watch?v=gxEPV4kolz0",
    "Ariel" : "https://www.youtube.com/watch?v=rBpaUICxEhk",
    "Jakob" : "https://www.youtube.com/watch?v=EBqCSseQXsI"
}


chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def saveName(name, url):
    cur = dbconn.cursor()
    cur.execute('INSERT INTO names(name, url) VALUES (%s, %s)', (name, url))
    cur.close()

def setLastChecked(a, b, c, d, e):
    cur = dbconn.cursor()
    cur.execute('UPDATE last_checked SET a=%s, b=%s, c=%s, d=%s, e=%s) WHERE id = 1',
        (a, b, c, d, e))
    cur.close()

def getLastChecked():
    cur = dbconn.cursor()
    cur.execute('SELECT a, b, c, d, e FROM last_checked WHERE id = 1')
    return cur.fetchone()

def tryWebsite(a, b, c, d, e):
    url = 'https://jul.dnb.no/v/' + a + b + c + d + e + '/'
    
    response = requests.get(url)
    code = response.status_code
    if code == 200:
        content = response.content

        firstPart = 'https://video.storm121.com/dnb-solvguttene-2021/result/thumbnails/thumb-'
        secondPart = '.mov.jpg\" /'

        strCont = str(content)
        start =strCont.find(firstPart) + len(firstPart)
        end =  strCont.find(secondPart)
        name = strCont[start:end]
        saveName(name, url)

async def send_message(client, message):
    print('Sending message: ' + message)
    channel = client.get_channel(851350540499943483)
    print ('Channel: ' + channel.name)
    await channel.send(message)

def checkName(client, name, url): 
    if name in friendNames:
        message = "God jul, " + friendNamesMap[name] + "!\n" + friendYoutubeMap[name] + "\n" + url
        print(message)
        #await send_message(client, message)

@tasks.loop(seconds=17.0)
async def checkNextBatch(client):
    abcde = getLastChecked()

    count = 0
    #adPHN
    for a in chars[chars.index(abcde[0]):]:
       for b in chars[chars.index(abcde[1]):]:
          for c in chars[chars.index(abcde[2]):]:
             for d in chars[chars.index(abcde[3]):]:
                    for e in chars[chars.index(abcde[4]):]:
                       tryWebsite(a, b, c, d, e)
                       count = count + 1
                       if count % 100 == 0:
                           setLastChecked(a, b, c, d, e)
                           print ('Count: ' + str(count) + ' : ' + a + b + c + d + e)
                           return           