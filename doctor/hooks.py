#!/usr/bin/env python
# encoding: utf-8

import doctor

def hookable(target, *args, **kwargs):
    def wrapper(*args, **kwargs):
        event = target.__name__
        if event in doctor.hookables:
            for hook in doctor.hookables[event]:
                try: hook(*args, **kwargs)
                except: pass
        return target(*args, **kwargs)
    return wrapper

class Hook:
    def __init__(self, f):
        event = self.__class__.__name__
        if event in doctor.hookables:
            doctor.hookables[event].append(f)
        else:
            doctor.hookables[event] = [f]

class message(Hook):         pass
class private_message(Hook): pass
class user_rename(Hook):     pass
class user_left(Hook):       pass
class user_joined(Hook):     pass
class user_quit(Hook):       pass
class user_kicked(Hook):     pass
class topic(Hook):           pass
class channel_mode(Hook):    pass
class user_mode(Hook):       pass
