#!/usr/bin/env python
# encoding: utf-8

import doctor
import re
import sys

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
        for script in doctor.config.scripts:
            self._load(script)

    def serialize(self, name):
        return re.sub(r'[^a-z]', '', name.lower())

    def _load(self, script):
        script = self.serialize(script)
        doctor.scripts.append(script)
        try:
            plugin = __import__('scripts.' + script, {}, {}, ['plugin'], 0)
            try: plugin._initialize()
            except: pass

            for func in dir(plugin):
                if func.startswith('command_'):
                    doctor.commands[func[len('command_'):]] = getattr(plugin, func)

        except: # Catch all for script errors
            pass
        return

    def _unload(self, script):
        script = self.serialize(script)
        doctor.scripts.remove(script)
        plugin = 'scripts.' + script

        try:
            for func in dir(sys.modules[plugin]):
                if func.startswith('command_'):
                    del doctor.commands[func[len('command_'):]]
            del sys.modules[plugin]
        except: pass

        return

    def load(self, plugin):
        self._load(plugin)

    def unload(self, plugin):
        doctor.hookables = {}

        plugin = self.serialize(plugin)

        for script in doctor.scripts:
            self._unload(script)

        doctor.scripts.remove(plugin)
        self.reload(unload=False)

    def reload(self, unload=True):
        doctor.hookables = {}

        for script in doctor.scripts:
            if unload: self._unload(script)
            self._load(script)
