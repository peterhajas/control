from bulbs import bulbs
import cherrypy

class ControlApp(object):
    allBulbs = bulbs.allBulbs()

    def index(self):
        return "Hello, world!"
    index.exposed = True

    @cherrypy.expose
    def off(self, name):
        print name
        bulb = bulbs.bulbWithName(self.allBulbs, name)
        bulb.turnOff()

    @cherrypy.expose
    def on(self, name):
        bulb = bulbs.bulbWithName(self.allBulbs, name)
        bulb.turnOn()

    @cherrypy.expose
    def allBulbNames(self):
        bulb_names = ""
        for bulb in self.allBulbs:
            name = bulb.name
            bulb_names = bulb_names + '\n' + name
        bulb_names = bulb_names[1:]
        return bulb_names

cherrypy.quickstart(ControlApp())
