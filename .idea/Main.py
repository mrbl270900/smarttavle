import json
import requests
import urllib.request
from urllib.request import urlopen
import pygame
from datetime import datetime


joke = ""
response = urlopen("https://v2.jokeapi.dev/joke/Any")
data_joke = json.loads(response.read())

url = urllib.request.urlopen("https://www.metaweather.com/api/location/554890/")  #weather in københavn
output = url.read().decode('utf-8')
raw_api_dict = json.loads(output)
url.close()
data_weather = raw_api_dict

if "joke" in data_joke:
    joke = data_joke["joke"]
else:
    joke = data_joke["setup"]
    joke = joke + " " + data_joke["delivery"]
while(len(joke)>100):
    response = urlopen("https://v2.jokeapi.dev/joke/Any")
    data_joke = json.loads(response.read())
    if "joke" in data_joke:
        joke = data_joke["joke"]
    else:
        joke = data_joke["setup"]
        joke = joke + " " + data_joke["delivery"]

weather = data_weather.get("consolidated_weather")[0].get("weather_state_name")
temp = str(data_weather.get("consolidated_weather")[0].get("the_temp"))

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 20)
timefont = pygame.font.SysFont('Helvetica', 50)


joketext = myfont.render("Todays joke:", False, (0, 0, 0))
thejoke = myfont.render(joke, False, (0, 0, 0))

weathertext = myfont.render("Weather in Copenhagen", False, (0, 0, 0))
theweather = myfont.render(weather + " and " + temp + " degrees out side", False, (0, 0, 0))

screen = pygame.display.set_mode([800, 200])
running = True
while running:


    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    time = timefont.render(current_time, False, (0,0,0))

    if(current_time == "23:59:59"):
        response = urlopen("https://v2.jokeapi.dev/joke/Any")
        data_joke = json.loads(response.read())
        if "joke" in data_joke:
            joke = data_joke["joke"]
        else:
            joke = data_joke["setup"]
            joke = joke + " " + data_joke["delivery"]
        while(len(joke)>100):
            response = urlopen("https://v2.jokeapi.dev/joke/Any")
            data_joke = json.loads(response.read())
            if "joke" in data_joke:
                joke = data_joke["joke"]
            else:
                joke = data_joke["setup"]
                joke = joke + " " + data_joke["delivery"]
        thejoke = myfont.render(joke, False, (0, 0, 0))

    for x in range(24):
        if(current_time == str(x) + ":20:00"):
            url = urllib.request.urlopen("https://www.metaweather.com/api/location/554890/")  #weather in københavn
            output = url.read().decode('utf-8')
            raw_api_dict = json.loads(output)
            url.close()
            data_weather = raw_api_dict
            weather = data_weather.get("consolidated_weather")[0].get("weather_state_name")
            temp = str(data_weather.get("consolidated_weather")[0].get("the_temp"))
            theweather = myfont.render(weather + " and " + temp + " degrees out side", False, (0, 0, 0))


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