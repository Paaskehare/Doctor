#!/usr/bin/env python
# encoding: utf-8
# Copyright (C) 2012 Ole Bergmann
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
#
# Ole Bergmann <ole@ole.im>

import sys
import time
from threading import Thread, Event

from doctor.irclib import nm_to_n, nm_to_h, irc_lower
from doctor.ircbot import SingleServerIRCBot
from doctor.hooks import hooks, hookable
from doctor.script import ScriptManager

import config

class OutputManager(Thread):
  def __init__(self, connection, delay=.5):
    Thread.__init__(self)
    self.setDaemon(1)
    self.connection = connection
    self.delay = delay
    self.event = Event()
    self.queue = []

  def run(self):
    while 1:
      self.event.wait()
      while self.queue:
        msg, target = self.queue.pop(0)
        self.connection.privmsg(target, msg)
        time.sleep(self.delay)
      self.event.clear()

  def send(self, msg, target):
    self.queue.append((msg.strip(), target))
    self.event.set()

class Client(SingleServerIRCBot):

  def __init__(self, nickname, server, channels):
    self._channels = channels
    self.nickname = nickname
    SingleServerIRCBot.__init__(self, [server], self.nickname, self.nickname)
    self.commands = {}
    self.queue = OutputManager(self.connection)
    self.queue.start()
    self.sm = ScriptManager(self, config.scripts)
    self.start()

  @hookable
  def on_welcome(self, c, e):
    for channel in self._channels:
      c.join(channel)

  @hookable
  def on_pubmsg(self, c, e):
    message = e.arguments()[0]
    source = e.source()
    channel = e.target()

    arguments = message.split(' ')
    print('%s > %s: %s' % (source, channel, message))
    if message.startswith(config.trigger):
      argument = arguments[0][1:]
      if argument == 'load':
        for arg in arguments[1:]:
          self.sm.load(arg)
      elif argument == 'unload':
        for arg in arguments[1:]:
          self.sm.unload(arg)
      elif argument == 'reload':
        for arg in arguments[1:]:
          self.sm.reload(arg)
      else:
        try: self.commands[argument](source, channel, arguments)
        except: pass

  def say(self, message, channel, show_prefix=True):
    self.queue.send((config.prefix + message if show_prefix else message), channel)
