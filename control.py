from bulbs import bulbs
import cherrypy
import os
import sys

configFilePath = sys.argv[1] + '.conf'
isDev = sys.argv[1] == 'dev'
ip = '10.0.1.3'

if isDev:
    ip = '127.0.0.1'

print ip

class ControlApp(object):
    def __init__(self):
        self.refreshBulbs()

    def refreshBulbs(self):
        self.allBulbs = bulbs.allBulbs()

    def index(self):
        panelFile = open('panel/index.html', 'r')
        panelContents = panelFile.read()
        panelFile.close()
        panelContents = panelContents.replace('ADDRESS', ip)
        return panelContents
    index.exposed = True

    def bulbWithName(self, name):
        # First, try to get one from self.allBulbs
        bulb = bulbs.bulbWithName(self.allBulbs, name)

        if bulb is None:
            # Refresh first
            self.refreshBulbs()
            bulb = bulbs.bulbWithName(self.allBulbs, name)

        return bulb

    @cherrypy.expose
    def off(self, name):
        bulb = self.bulbWithName(name)
        bulb.turnOff()

    @cherrypy.expose
    def on(self, name):
        bulb = self.bulbWithName(name)
        bulb.turnOn()

    @cherrypy.expose
    def toggle(self, name):
        bulb = self.bulbWithName(name)
        bulb.toggle()

    @cherrypy.expose
    def allBulbNames(self):
        self.refreshBulbs()
        bulb_name_list = [ ]
        bulb_names = ""

        for bulb in self.allBulbs:
            name = bulb.name
            bulb_name_list.append(name)

        bulb_name_list.sort()

        for name in bulb_name_list:
            bulb_names = bulb_names + '\n' + name

        bulb_names = bulb_names[1:]

        return bulb_names

cherrypy.quickstart(ControlApp(), '/', configFilePath)
