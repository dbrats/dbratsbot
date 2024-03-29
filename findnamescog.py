import requests
import psycopg2
from psycopg2.extras import RealDictCursor
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
    password=PASSWORD,
    cursor_factory=RealDictCursor
)

friendNames = ["Theodor"]

friendNamesMap = {
    "Theodor" : "<@120114285845282817>"
}

friendYoutubeMap = {
    "Theodor" : "https://www.youtube.com/watch?v=qzEoBrr9gRA"
}

chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def saveName(name, url):
    cur = dbconn.cursor()
    cur.execute('INSERT INTO names(name, url) VALUES (%s, %s)', (name, url))
    dbconn.commit()
    cur.close()

def setLastChecked(a, b, c, d, e):
    cur = dbconn.cursor()
    cur.execute('UPDATE last_checked SET a=%s, b=%s, c=%s, d=%s, e=%s WHERE id = 1', (a, b, c, d, e))
    dbconn.commit()
    cur.close()

def getLastChecked():
    cur = dbconn.cursor()
    cur.execute('SELECT a, b, c, d, e FROM last_checked WHERE id = 1')
    result = cur.fetchone()
    lastChecked = (result['a'], result['b'], result['c'], result['d'], result['e'])
    cur.close()
    return lastChecked

async def tryWebsite(a, b, c, d, e, client):
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
        await checkName(client, name, url)

async def send_message(client, message):
    print('Sending message: ' + message)
    channel = client.get_channel(851350540499943483)
    print ('Channel: ' + channel.name)
    await channel.send(message)

async def checkName(client, name, url):
    print("Checking name: " + name)
    if name in friendNames:
        message = "God jul, " + friendNamesMap[name] + "!\n" + friendYoutubeMap[name] + "\n" + url
        await send_message(client, message)

def doStartFromLogic(currentChar, lastChecked, lastCheckedIdx):
    if chars.index(currentChar) < chars.index(lastChecked[lastCheckedIdx]):
        return True
    elif chars.index(currentChar) == chars.index(lastChecked[lastCheckedIdx]):
        lastChecked[lastCheckedIdx] = chars[0]
    return False

@tasks.loop(seconds=15.0)
async def checkNextBatch(client):
    lastChecked = list(getLastChecked())

    print ("Checking: " + str(lastChecked))

    count = 0
    for a in chars:
        if doStartFromLogic(a, lastChecked, 0):
            continue
        for b in chars:
            if doStartFromLogic(b, lastChecked, 1):
                continue
            for c in chars:
                if doStartFromLogic(c, lastChecked, 2):
                    continue
                for d in chars:
                    if doStartFromLogic(d, lastChecked, 3):
                        continue
                    for e in chars:
                        if doStartFromLogic(e, lastChecked, 4):
                            continue
                        count = count + 1
                        await tryWebsite(a, b, c, d, e, client)
                        if count % 100 == 0:
                            setLastChecked(a, b, c, d, e)
                            print ('Count: ' + str(count) + ' : ' + a + b + c + d + e)
                            return