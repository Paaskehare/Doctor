#!/usr/bin/env python
# encoding: utf-8

import config

from doctor.script import ScriptManager, Alias

from doctor.hooks import \
    message \
  , private_message \
  , user_rename \
  , user_left \
  , user_joined \
  , user_quit \
  , user_kicked \
  , topic \
  , channel_mode \
  , user_mode

hookables = {}
scripts   = []
commands  = {}

script_manager = ScriptManager()
