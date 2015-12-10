from bulbs import bulbs
import cherrypy
import os
import sys
import time

configFilePath = sys.argv[1] + '.conf'
isDev = sys.argv[1] == 'dev'
ip = '10.0.1.3'

if isDev:
    ip = '127.0.0.1'

class ControlApp(object):
    def __init__(self):
        self.bulbManager = bulbs.BulbManager()

    def index(self):
        panelFile = open('panel/index.html', 'r')
        panelContents = panelFile.read()
        panelFile.close()
        panelContents = panelContents.replace('ADDRESS', ip)
        return panelContents
    index.exposed = True

    def bulbWithName(self, name):
        return self.bulbManager.bulbWithName(name)

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
    def state(self, name):
        bulb = self.bulbWithName(name)
        if bulb.isOn():
            return 'on'
        else:
            return 'off'

    @cherrypy.expose
    def perceivedColor(self, name):
        bulb = self.bulbWithName(name)
        return bulb.perceivedColor()

    @cherrypy.expose
    def allBulbNames(self):
        bulb_name_list = [ ]
        bulb_names = ''
        for bulb in self.bulbManager.bulbs():
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
app = ControlApp()

cherrypy.tree.mount(app, '/', configFilePath)
cherrypy.engine.start()

