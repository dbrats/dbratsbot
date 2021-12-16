import requests

def tryWebsite(a, b, c, d, e):
    url = 'https://jul.dnb.no/v/' + a + b + c + d + e + '/'
    
    response = requests.get(url)
    code = response.status_code
    if code == 200:
        #<meta property="og:image" content="https://video.storm121.com/dnb-solvguttene-2021/result/thumbnails/thumb-Vegard.mov.jpg" />
        content = response.content

        firstPart = 'https://video.storm121.com/dnb-solvguttene-2021/result/thumbnails/thumb-'
        secondPart = '.mov.jpg\" /'

        strCont = str(content)
        start =strCont.find(firstPart) + len(firstPart)
        end =  strCont.find(secondPart)
        name = strCont[start:end]

        f = open("names.txt", "a")
        f.write(name + ' : ' + url + '\n')
        f.close()
    return False

chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

count = 0
#adPHN
for a in chars:
    for b in chars[3:]:
        for c in chars[41:]:
            for d in chars[33:]:
                for e in chars[39:]:
                    count = count + 1
                    if count % 100 == 0:
                        print ('Count: ' + str(count) + ' : ' + a + b + c + d + e)
                    quit = tryWebsite(a, b, c, d, e)
                    if quit:
                        print (a + b + c + d + e)
                        exit()

print (count)
                    
print ('Finished.')
exit()