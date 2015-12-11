# -*- coding: UTF-8 -*-

import yaml
import subprocess
import time

def _stdOutFromFluxCommand(argsList):
    command = 'python bulbs/flux_led.py ' + argsList
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    stdOut = process.communicate()[0]
    return stdOut

bulbUpdateThreshold = 30

class BulbManager:
    def __init__(self):
        self._bulbs = [ ]
        self.lastBulbUpdateTime = time.time()
        self._updateBulbs()

    def bulbWithName(self, name):
        for bulb in self.bulbs():
            if bulb.name == name:
                return bulb
        return None

    def bulbs(self):
        now = time.time()
        difference = now - self.lastBulbUpdateTime

        if difference > bulbUpdateThreshold:
            self._updateBulbs
            self.lastBulbUpdateTime = now

        return self._bulbs

    def _updateBulbs(self):
        data = _stdOutFromFluxCommand('-s')
        data = data.split('\n')[1:-1]

        data = [entry.strip() for entry in data]

        # Reverse the name-to-ip map
        names_to_udids_file = open('bulbs/bulbs.yaml', 'r')
        names_to_udids = yaml.load(names_to_udids_file)
        udids_to_names = { }

        for key in names_to_udids.keys():
            udid = names_to_udids[key]
            udids_to_names[udid] = key

        bulbs = [ ]

        for bulbData in data:
            udid = bulbData.split(' ')[0]
            ip = bulbData.split(' ')[1]

            if udid in udids_to_names.keys():
                name = udids_to_names[udid]
            else:
                name = udid
            bulb = Bulb(name, udid, ip)
            bulbs.append(bulb)

        names_to_udids_file.close()

        # Sort the bulbs by name
        bulbs = sorted(bulbs, key=lambda Bulb: Bulb.name)

        self._bulbs = bulbs

class Bulb:
    def __init__(self, name, udid, ip):
        self.name = name
        self.ip = ip

    def _currentStatusString(self):
        status = _stdOutFromFluxCommand('-i {}'.format(self.ip))
        status = status.replace('[{}]'.format(self.ip), '')
        status = status.strip()

        return status

    def isOn(self):
        status = self._currentStatusString()
        statusStateElement = status.split()[0]
        statusStateElement = statusStateElement.strip()

        if statusStateElement == "ON":
            return True
        elif statusStateElement == "OFF":
            return False
        else:
            print "Unknown state - assuming \"OFF\""
            return False

    def setOn(self, on):
        onDirective = ''
        if on:
            onDirective = "1"
        else:
            onDirective = "0"
        command = '-{} {}'.format(onDirective, self.ip)
        _stdOutFromFluxCommand(command)

    def turnOn(self):
        self.setOn(True)

    def turnOff(self):
        self.setOn(False)

    def toggle(self):
        newOn = not self.isOn()
        self.setOn(newOn)

    def perceivedColor(self):
        stateStr = self._currentStatusString()

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

