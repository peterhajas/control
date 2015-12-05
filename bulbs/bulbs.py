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

    def perceivedColor(self):
        self.wifiLEDBulb.refreshState()
        self.wifiLEDBulb.refreshState()
        stateStr = self.wifiLEDBulb.__str__()

        # Shave off the first part ("ON or "OFF")

        firstElement = stateStr.split(' ')[0]
        colorStr = stateStr.replace(firstElement, '')

        # Remove colons, percent signs, commas and parens

        colorStr = colorStr.replace(':', '')
        colorStr = colorStr.replace('%', '')
        colorStr = colorStr.replace(',', '')
        colorStr = colorStr.replace('(', '')
        colorStr = colorStr.replace(')', '')

        # Strip leading / trailing whitespace

        colorStr = colorStr.strip()

        # Strip leading / trailing brackets

        colorStr = colorStr.strip('[')
        colorStr = colorStr.strip(']')

        def stripHex(hexStr):
            return hexStr.replace('0x', '')

        if colorStr.find('Warm White') > -1:
            colorStr = colorStr.replace('Warm White', '')
            colorStr = colorStr.strip()

            # Convert the percent string into a CSS-style component element
            component = int((0.01 * float(colorStr)) * 255)
            component = stripHex(hex(component))

            colorStr = '#' + component * 3
        elif colorStr.find('Color') > -1:
            colorStr = colorStr.replace('Color', '')
            colorStr = colorStr.strip()

            components = colorStr.split(' ')

            print components

            if len(components) > 2:
                # Grab the three components
                r = stripHex(hex(int(components[0])))
                g = stripHex(hex(int(components[1])))
                b = stripHex(hex(int(components[2])))

                def elongateComponentIfNeeded(component):
                    if len(component) < 2:
                        return 2 * component
                    else:
                        return component

                r = elongateComponentIfNeeded(r)
                g = elongateComponentIfNeeded(g)
                b = elongateComponentIfNeeded(b)

                colorStr = '#' + r + g + b
            else:
                # It's a CSS color
                return colorStr
        else:
            # If the pattern is "Unknown", default to RGB for the on/off state
            
            if self.isOn():
                colorStr = '#FFFFFF'
            else:
                colorStr = '#000000'

        return colorStr

