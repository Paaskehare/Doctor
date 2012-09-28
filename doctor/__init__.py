#!/usr/bin/env python
# encoding: utf-8

import os, logging

from doctor.script  import ScriptManager, Alias
from doctor.storage import Storage
from doctor.doctor  import Doctor

# Re-mapping of hook aliases to the root module
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

# Containers for various scripting functionionality
prefix    = '\x034>\x0F '
trigger   = '!', '.',
scripts   = []

hookables = {}
commands  = {}

# Instantiate the scripting manager variable
script_manager = None 

# Logging format
logging.basicConfig(format='%(asctime)s \033[1m%(levelname)s\033[0m  %(message)s', level=logging.DEBUG, datefmt='%H:%M:%S')

# Instantiate the multiprocessing pool variable
pool = None

directory = os.getcwd()
