import json
import requests
import urllib.request
from urllib.request import urlopen
import pygame



joke = ""
response = urlopen("https://v2.jokeapi.dev/joke/Any")
data_joke = json.loads(response.read())

url = urllib.request.urlopen("https://www.metaweather.com/api/location/554890/")  #weather in københavn
output = url.read().decode('utf-8')
raw_api_dict = json.loads(output)
url.close()
data_weather = raw_api_dict
print(data_joke)
print(data_weather)

if "joke" in data_joke:
    joke = data_joke["joke"]
else:
    joke = data_joke["setup"]
    joke = joke + " " + data_joke["delivery"]



weather = data_weather.get("consolidated_weather")[0].get("weather_state_name")
print(weather)

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Helvetica', 15)
joketext = myfont.render("Todays joke:", False, (0, 0, 0))
thejoke = myfont.render(joke, False, (0, 0, 0))

theweather = myfont.render(weather, False, (0, 0, 0))
screen = pygame.display.set_mode([1000, 1000])
running = True
while running:

    screen.fill((255,255,255))
    screen.blit(joketext,(5,0))
    screen.blit(thejoke,(5,20))
    screen.blit(theweather,(5,65))
    pygame.display.flip()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False