import json
import urllib.request
from urllib.request import urlopen
import pygame
from datetime import datetime
#her importeres vores liberys

def getNews(): #denne funktion henter nyheder fra newsapi
    response = urlopen("https://newsapi.org/v2/top-headlines?country=us&apiKey=b23f98a3a2ee49a1b35b8840adf63a72")
    data_news = json.loads(response.read())
    return data_news;

def getArticel(data_news, x): #denne funktion får overskriften fra articel x
    text = str(data_news["articles"][x]["title"])
    return text

def getArticeltext(data_news, x): #denne funktion henter de første 110 chars af articel x's description
    text = str(data_news["articles"][x]["description"])
    text2=""
    if(len(text)>100):
        text2 = text[:110]
    return text2

def getArticeltext2(data_news, x): #Samme som over ud over at den henter chars mellem 110 og 220
    text = str(data_news["articles"][x]["description"])
    text3 = ""
    if(len(text)>110):
        text3 =text[110:220]
    return text3
def getArticeltext3(data_news, x): #samme som over men henter chars efter 220
    text = str(data_news["articles"][x]["description"])
    text4 = ""
    if(len(text)>220):
        text4 =text[220:]
    return text4

def chekJoke(data_joke): #denne funktion chekker at JSON structuren i data_joke er enten som joke eller som setup og delivery og retunere joken
    if "joke" in data_joke:
        joke = data_joke["joke"]
    else:
        joke = data_joke["setup"]
        joke = joke + " " + data_joke["delivery"]
    return joke

def getJoke(): #denne funktion henter en ny joke og chekker om den er under 110 chars ellers henter den en ny derudover kalder den også chekjoke
    response = urlopen("https://v2.jokeapi.dev/joke/Any")
    data_joke = json.loads(response.read())
    joke = str(chekJoke(data_joke))
    while(len(joke)>110):
        response = urlopen("https://v2.jokeapi.dev/joke/Any")
        data_joke = json.loads(response.read())
        chekJoke(data_joke)
    return joke

def getTime():#denne funktion for tiden og retunere den
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def getWeather(): # denne henter verjet og retunere weather state samt de første 5 chars af temp
    url = urllib.request.urlopen("https://www.metaweather.com/api/location/554890/")  #weather in københavn
    output = url.read().decode('utf-8')
    raw_api_dict = json.loads(output)
    url.close()
    data_weather = raw_api_dict
    weather = data_weather.get("consolidated_weather")[0].get("weather_state_name")
    temp = str(data_weather.get("consolidated_weather")[0].get("the_temp"))
    tempHolder = ""
    for x in temp:
        tempHolder = tempHolder + x
        if(len(tempHolder)>4):
            temp = tempHolder
            break

    return weather + " and " + temp + " degrees out side";

pygame.init() #her intitere vi vores pygame samt vores fonter
pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 20)
timefont = pygame.font.SysFont('Helvetica', 50, bold=True)
Overskrift = pygame.font.SysFont('Helvetica', 20, bold=True)


joketext = Overskrift.render("Todays joke:", False, (0, 0, 0)) #under her rendere vi vores text første gang
thejoke = myfont.render(getJoke(), False, (0, 0, 0))

weathertext = Overskrift.render("Weather in Copenhagen", False, (0, 0, 0))
theweather = myfont.render(getWeather(), False, (0, 0, 0))

news_data = getNews() #her hentes news
newsHeadline = Overskrift.render(getArticel(news_data,0), False, (0, 0, 0))
newsText = myfont.render(getArticeltext(news_data,0), False, (0, 0, 0))
newsText2 = myfont.render(getArticeltext2(news_data,0), False, (0, 0, 0))
newsText3 = myfont.render(getArticeltext3(news_data,0), False, (0, 0, 0))

screen = pygame.display.set_mode([1000, 300]) # screen startes samt sætter running to true
running = True
while running: #her startes vores whille loop
    time = timefont.render(getTime(), False, (0,0,0))#hvert loop sætter vi tiden

    if(getTime() == "23:59:59"): # hvis tiden er 23.59.59 så henter en ny joke og sender den til render
        thejoke = myfont.render(getJoke(), False, (0, 0, 0))

    for x in range(24): #her kigger vi på tal fra 0 til 23 og hvis tiden er en af dem så henter vi verjet igen
        if(getTime() == str(x) + ":00:00"):
            theweather = myfont.render(getWeather(), False, (0, 0, 0))
        for y in range(30): #her kigger vi på tal fra 0 til 29 og hvis det gange 2 samt timen over passer med tiden henter vi nye nyheder
            z = y*2
            if(getTime() == str(x) + ":" + str(z) + ":00"):
                news_data = getNews()
                newsHeadline = Overskrift.render(getArticel(news_data,0), False, (0, 0, 0))
                newsText = myfont.render(getArticeltext(news_data,0), False, (0, 0, 0))
                newsText2 = myfont.render(getArticeltext2(news_data,0), False, (0, 0, 0))
                newsText3 = myfont.render(getArticeltext3(news_data,0), False, (0, 0, 0))

    screen.fill((255,255,255)) #her fyldes baggrunden med hvid

    screen.blit(time,(0,0)) #disse blit bruges til at sende vores renders til screen
    screen.blit(joketext,(5,50))
    screen.blit(thejoke,(5,70))
    screen.blit(weathertext,(5,95))
    screen.blit(theweather,(5,115))
    screen.blit(newsHeadline,(5,140))
    screen.blit(newsText,(5,160))
    screen.blit(newsText2,(5,180))
    screen.blit(newsText3,(5,200))
    pygame.display.flip() #her tager alle blit og vises på skærmen

    pygame.time.delay(500) #dette delay er så vi kun henter nyheder en gang når der er gået 2 min ellers ville vi hente nyheder 10 gange på et sekund

    for event in pygame.event.get(): # dette bruges til at stoppe pogramet når man trykker på krydset i pygame vinduet
        if event.type == pygame.QUIT:
            running = False