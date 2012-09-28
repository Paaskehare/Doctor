#!/usr/bin/env python

import doctor
from doctor.irc      import Network
from doctor.script   import ScriptManager

from multiprocessing import Queue, Process

import logging
import multiprocessing

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
           ) for network in options['networks'] 
        ]

        doctor.trigger  = options.get('trigger', doctor.trigger)
        doctor.prefix   = options.get('prefix',   doctor.prefix)
        doctor.scripts  = options.get('scripts',  doctor.scripts)

        doctor.script_manager = ScriptManager()

    def run(self):


        def worker(q, network):
            q.put(network.run(), False)

            # Make for a clean exit so we can save the storage:
            if q.empty():
                # save the storage objects for scripts
                doctor.script_manager.exit()

        q = Queue()
        for network in self.networks:
            p = Process(target=worker, args=(q, network,))
            p.start()

