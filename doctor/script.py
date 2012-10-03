#!/usr/bin/env python
# encoding: utf-8

import doctor
import re
import sys

from copy import copy
from traceback import extract_tb

logging = doctor.logging

# Decorator for aliasing commands
class Alias:
    def __init__(self, *aliases):
        self.aliases = aliases

    def __call__(self, f):
        for alias in self.aliases:
            doctor.commands[alias] = f
        def wrapper(*args, **kwargs):
            f(*args)
        return wrapper

class ScriptManager:

    script_dir = 'scripts.'

    def __init__(self):
        self.loaded = []
        for script in doctor.scripts:
            self._load(script)

    def serialize(self, name):
        return re.sub(r'[^a-z]', '', name.lower())

    def _load(self, script):
        script = self.serialize(script)

        doctor.logging.debug('- %s "Loading %s"' % ('SCRIPT'.ljust(8), script))

        try:
            plugin = __import__(self.script_dir + script, {}, {}, ['plugin'], 0)

            for func in dir(plugin):
                if func.startswith('command_'):
                    doctor.commands[func[len('command_'):]] = getattr(plugin, func)

            self.loaded.append(script)
            doctor.logging.debug('- %s "Successfully Loaded %s"' % ('SCRIPT'.ljust(8), script))
        
        except BaseException as exc: # Catch all for script errors
            traceback = extract_tb(exc.__traceback__)
            for e in traceback:
                f, l, m, s = e

                # only catch errors for the script
                if f.endswith('%s.py' % script):
                    logging.warning('File "%s", line %s, in %s' % (f, l, m))
                    logging.warning('  %s' % s)

                logging.warning('%s: %s' % (exc.__class__.__name__, exc))
        except: # Error cannot be caught, just pass
            pass
        return

    def _unload(self, script):
        script = self.serialize(script)

        doctor.logging.debug('- %s "Unloading %s"' % ('SCRIPT'.ljust(8), script))

        try:
            plugin = sys.modules.get(self.script_dir + script, None)
            if plugin:
                for func in dir(plugin):
                    f = getattr(plugin, func)
                    if type(f) is doctor.Storage:
                        f._write_file()
                
                del sys.modules[self.script_dir + script]
                self.loaded.remove(script)
        except:
            pass

        return

    def unload_all(self):
        for script in self.loaded:
            self._unload(script)
        self.loaded = []

    def load(self, plugin):
        self._load(plugin)

    def unload(self, script):
        self._unload(script)
        self.scripts.remove(script)
        self.reload()

    def reload(self):
        loaded = copy(self.loaded)
        doctor.hookables = {} # wipe and re-assign all hooks
        doctor.commands  = {} # wipe and re-assign all commands

        for script in loaded:
            self._unload(script)
            self._load(script)

        doctor.logging.debug('- %s "Reloaded scripts"' % ('SCRIPT'.ljust(8)))
