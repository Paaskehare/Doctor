#!/usr/bin/env python
# encoding: utf-8

import config
import logging

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

logging.basicConfig(format='%(asctime)s \033[1m%(levelname)s\033[0m  %(message)s', level=logging.DEBUG, datefmt='%H:%M:%S')
