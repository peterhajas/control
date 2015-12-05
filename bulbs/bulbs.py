import flux_led
import yaml

class BulbManager:
    def __init__(self):
        self.bulbs = [ ]
        self._updateBulbs()

    def bulbWithName(self, name):
        for bulb in self.bulbs:
            if bulb.name == name:
                return bulb
        return None

    def _updateBulbs(self):
        seeker = flux_led.BulbSeeker()
        ips = seeker.discover(5)

        # Reverse the name-to-ip map
        names_to_ips_file = open('bulbs/bulbs.yaml', 'r')
        names_to_ips = yaml.load(names_to_ips_file)
        ips_to_names = { }

        for key in names_to_ips.keys():
            ip = names_to_ips[key]
            ips_to_names[ip] = key

        bulbs = [ ]

        for ip in ips:
            if ip in ips_to_names.keys():
                name = ips_to_names[ip]
            else:
                name = ip
            bulb = Bulb(name, ip)
            bulbs.append(bulb)

        names_to_ips_file.close()

        self.bulbs = bulbs

class Bulb:
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.wifiLEDBulb = flux_led.WifiLedBulb(ip)
        self.wifiLEDBulb.refreshState()

    def isOn(self):
        self.wifiLEDBulb.refreshState()
        return self.wifiLEDBulb.is_on

    def setOn(self, on):
        self.wifiLEDBulb.turnOn(on)

    def turnOn(self):
        self.setOn(True)

    def turnOff(self):
        self.setOn(False)

    def toggle(self):
        newOn = not self.isOn()
        self.setOn(newOn)

