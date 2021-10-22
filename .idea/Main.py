import json
import requests
from urllib.request import urlopen
import pygame


response = urlopen("https://v2.jokeapi.dev/joke/Any")
data_json = json.loads(response.read())

print(data_json["setup"])
print(data_json["delivery"])


pygame.init()
screen = pygame.display.set_mode([500, 500])
running = True
while running:

    screen.fill("white")
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False