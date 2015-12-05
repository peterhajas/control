import time
import os
import sys
import requests
from PyEcho import *

isDev = sys.argv[1] == 'dev'

if isDev:
    ip = '127.0.0.1'
else:
    ip = '10.0.1.3'

echo = PyEcho.PyEcho('MY_AMAZON_EMAIL', 'MY_AMAZON_PASSWORD')

def _urlBase():
    return 'http://{}:8080/'.format(ip)

def toggleBulb(name):
    url = _urlBase() + 'toggle/{}'.format(name)
    requests.get(url)

def allBulbNames():
    url = _urlBase() + 'allBulbNames'
    request = requests.get(url)
    text = str(request.text)

    bulbNames = text.split('\n')
    return bulbNames

bulbs = [ ]

def refreshBulbs():
    global bulbs
    bulbs = allBulbNames()

secondsToRefreshAfter = 30
secondsElapsedSinceRefresh = 0

refreshBulbs()

while True:
    secondsElapsedSinceRefresh += 1

    if secondsElapsedSinceRefresh > secondsToRefreshAfter:
        secondsElapsedSinceRefresh = 0
        refreshBulbs()

    tasks = echo.tasks()

    for task in tasks:
        text = task['text']
        taskElements = text.split(' ')

        print 'Parsing Alexa text {}'.format(text)

        for taskElement in taskElements:
            for bulbName in bulbs:
                bulbNameElements = bulbName.split(' ')
                for bulbNameElement in bulbNameElements:
                    if bulbNameElement in taskElement:
                        print 'Found bulb {}'.format(bulbName)
                        toggleBulb(bulbName)

        echo.deleteTask(task)

    time.sleep(1)
