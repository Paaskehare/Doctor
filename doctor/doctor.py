#!/usr/bin/env python

import doctor
from doctor.irc    import Network
from doctor.script import ScriptManager

class Doctor:
    def __init__(self, options):
        if not options.get('networks'):
            print('No networks defined, exiting ..')
            return

        self.networks   = [
           Network(
               host     = network.get('host'),
               port     = network.get('port',     6667),
               nick     = network.get('nick'),
               ident    = network.get('ident', ''),
               realname = network.get('realname', ''),
               channels = network.get('channels', []),
           ) for network in options['networks'] # We can only use the first network as of now
        ]

        doctor.trigger  = options.get('trigger', doctor.trigger)
        doctor.prefix   = options.get('prefix',   doctor.prefix)
        doctor.scripts  = options.get('scripts',  doctor.scripts)

        doctor.script_manager = ScriptManager()

    def run(self):
        for network in self.networks:
           network.run()
