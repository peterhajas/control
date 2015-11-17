import flux_led

class Bulb:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.wifiLEDBulb = flux_led.WifiLedBulb(ip)
        self.wifiLEDBulb.refreshState()

    def isOn(self):
        return self.wifiLEDBulb.isOn()

    def setOn(self, on):
        self.wifiLEDBulb.turnOn(on)

    def turnOn(self):
        self.setOn(True)

    def turnOff(self):
        self.setOn(False)

    def toggle(self):
        newOn = not self.isOn
        self.setOn(newOn)

def allBulbs():
    seeker = flux_led.BulbSeeker()
    ips = seeker.discover(5)

    bulbs = [ ]

    for ip in ips:
        bulb = Bulb("Bulb", ip)
        bulbs.append(bulb)

    return bulbs
