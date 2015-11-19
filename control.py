from bulbs import bulbs
import cherrypy
import os

class ControlApp(object):
    def __init__(self):
        self.refreshBulbs()

    def refreshBulbs(self):
        self.allBulbs = bulbs.allBulbs()

    def index(self):
        panelFile = open('panel/index.html', 'r')
        panelContents = panelFile.read()
        panelFile.close()
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

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': 8080,
                       })
cherrypy.quickstart(ControlApp(), '/', 'control.conf')
