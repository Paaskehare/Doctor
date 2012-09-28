#!/usr/bin/env python
# encoding: utf-8

import doctor
import re
import sys

from copy import copy

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
    def __init__(self):
        for script in doctor.scripts:
            self._load(script)

    def serialize(self, name):
        return re.sub(r'[^a-z]', '', name.lower())

    def _load(self, script):
        script = self.serialize(script)
        doctor.loaded.append(script)
        try:
            plugin = __import__('scripts.' + script, {}, {}, ['plugin'], 0)
            # if the script has an init function, execute it
            try: plugin._init() 
            except: pass

            for func in dir(plugin):
                if func.startswith('command_'):
                    doctor.commands[func[len('command_'):]] = getattr(plugin, func)

        except: # Catch all for script errors
            pass
        return

    def _unload(self, script):
        script = self.serialize(script)
        doctor.loaded.remove(script)
        plugin = 'scripts.' + script
        doctor.logging.debug('- %s "Unloading %s"' % ('SCRIPT'.ljust(8), script))

        try:
            for func in dir(sys.modules[plugin]):
                if func.startswith('command_'):
                    del doctor.commands[func[len('command_'):]]
            del sys.modules[plugin]
        except: pass

        return

    def exit(self):
        loaded = copy(loaded)
        for script in loaded:
            self._unload(script)
        doctor.loaded = []

    def load(self, plugin):
        self._load(plugin)
        doctor.logging.debug('- %s "Loaded %s"' % ('SCRIPT'.ljust(8), plugin))

    def unload(self, plugin):
        plugin = self.serialize(plugin)

        for script in doctor.loaded:
            self._unload(script)

        doctor.loaded.remove(plugin)
        self.reload()

    def reload(self):
        doctor.logging.debug('- %s "Reloaded scripts"' % ('SCRIPT'.ljust(8)))
        doctor.hookables = {}

        for script in doctor.loaded:
            self._unload(script)
            self._load(script)
