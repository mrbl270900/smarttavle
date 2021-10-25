import json
import requests
import urllib.request
from urllib.request import urlopen
import pygame
from datetime import datetime

def chekJoke(data_joke):
    if "joke" in data_joke:
        joke = data_joke["joke"]
    else: # else put botehe the setup an delivery in the joke varibul
        joke = data_joke["setup"]
        joke = joke + " " + data_joke["delivery"]
        return joke

def getJoke():
    response = urlopen("https://v2.jokeapi.dev/joke/Any")
    data_joke = json.loads(response.read())
    joke = str(chekJoke(data_joke))
    while(len(joke)>100):
        response = urlopen("https://v2.jokeapi.dev/joke/Any")
        data_joke = json.loads(response.read())
        chekJoke(data_joke)
    return joke

def getTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return current_time

def getWeather():
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

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 20)
timefont = pygame.font.SysFont('Helvetica', 50)


joketext = myfont.render("Todays joke:", False, (0, 0, 0))
thejoke = myfont.render(getJoke(), False, (0, 0, 0))

weathertext = myfont.render("Weather in Copenhagen", False, (0, 0, 0))
theweather = myfont.render(getWeather(), False, (0, 0, 0))

screen = pygame.display.set_mode([800, 200])
running = True
while running:
    time = timefont.render(getTime(), False, (0,0,0))

    if(getTime() == "23:59:59"):
        thejoke = myfont.render(getJoke(), False, (0, 0, 0))

    for x in range(24):
        if(getTime() == str(x) + ":00:00"):
            theweather = myfont.render(getWeather(), False, (0, 0, 0))

    screen.fill((255,255,255))

    screen.blit(time,(0,0))
    screen.blit(joketext,(5,50))
    screen.blit(thejoke,(5,70))
    screen.blit(weathertext,(5,95))
    screen.blit(theweather,(5,115))
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False