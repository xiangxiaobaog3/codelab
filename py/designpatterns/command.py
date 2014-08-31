#!/usr/bin/env python
# encoding: utf-8

class Switch:
    """The Invoker class"""

    def __init__(self, flipUpCmd, flipDownCmd):
        self.__flipDownCmd = flipDownCmd
        self.__flipUpCmd = flipUpCmd

    def flipUp(self):
        self.__flipUpCmd.execute()

    def flipDown(self):
        self.__flipDownCmd.execute()


class Light:
    """The Receiver class"""

    def turnOn(self):
        print "The light is on"

    def turnOff(self):
        print "The light is off"


class Command:
    """The Command Abstract class"""

    def __init__(self):
        pass

    def execute(self):
        raise NotImplemented


class FlipUpCommand(Command):
    def __init__(self, light):
        self.__light = light

    def execute(self):
        self.__light.turnOn()


class FlipDownCommand(Command):
    def __init__(self, light):
        self.__light = light

    def execute(self):
        self.__light.turnOff()


class LightSwitch:
    """The Client Class"""

    def __init__(self):
        self.__lamp = Light()
        self.__switchUp = FlipUpCommand(self.__lamp)
        self.__switchDown = FlipDownCommand(self.__lamp)
        self.__switch = Switch(self.__switchUp, self.__switchDown)

    def switch(self, cmd):
        _switch = {
            'ON': self.__switch.flipUp,
            'OFF': self.__switch.flipDown,
        }
        cmd = cmd.strip().upper()
        _switch[cmd]()


def main():
    lightSwitch = LightSwitch()
    print 'Switch ON test.'
    lightSwitch.switch('ON')

    print 'Switch OFF test.'
    lightSwitch.switch('OFF')

if __name__ == '__main__':
    main()
