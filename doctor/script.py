#!/usr/bin/env python
# encoding: utf-8

import doctor

import re
import sys

doctor.loaded = []

try:
  import scripts
except ImportError:
  pass

class ScriptManager:
  def __init__(self, bot, scripts):
    self.bot = bot
    for script in scripts:
      self._load(script)

  def serialize(self, name):
    return re.sub(r'[^a-z]', '', name.lower())

  def _load(self, script):
    script = self.serialize(script)
    doctor.loaded.append(script)
    try:
      mod = __import__('scripts.'+script, {}, {}, ['mod'], 0)
      mod.bot = self.bot
      try: mod._init()
      except: pass
      for func in dir(mod):
        if func.startswith('command_'):
          self.bot.commands[func[len('command_'):]] = getattr(mod, func)
      print('* Successfully imported ', script)
    except:
      print('import error')
      pass

  def _unload(self, script):
    script = self.serialize(script)
    doctor.loaded.remove(script)
    mod = 'scripts.' + script
    try:
      print(dir(sys.modules[mod]))
      for func in dir(sys.modules[mod]):
        if func.startswith('command'):
          del self.bot.commands[func[len('command_'):]]
      del sys.modules[mod]
    except:
      pass

  def reload(self):
    doctor.hooks = {}
    # Reset hooks so we can hook them again on reload
    for script in doctor.loaded:
      self._unload(script)
      self._load(script)
