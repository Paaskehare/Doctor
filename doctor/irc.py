#!/usr/bin/env python
# encoding: utf-8

import socket
import logging
import ssl

import config
import doctor

from doctor.hooks import hookable

logging = doctor.logging

_valid_user_flag = '+', '@', '%', '&', '~', 'q'

class User:
    nick      = ""
    ident     = ""
    host      = ""
    flags     = ""
    channels  = []

    network = None

    def __repr__(self):  return self.nick

    def __init__(self, network, nick, flags='', ident='', host=''):
        self.network  = network
        self.ident    = ident
        self.host     = host

        for flag in flags:
            self.flags += self.prefix_to_flag(flag)

        if nick.startswith(_valid_user_flag):
            self.flags += self.prefix_to_flag(nick[0])
            nick = nick[1:]

        self.nick = nick

    def say(self, message):
        message = ':' + message
        self.network.send('PRIVMSG', self.nick, message)

    def prefix_to_flag(self, prefix):
        return {
          '+': 'v',
          '@': 'o',
          '%': 'h',
          '&': 'a',
          '~': 'q',
        }.get(prefix, '')

class Channel:
    name = ""
    users = []

    network = None

    def __repr__(self):  return self.name

    def __init__(self, network, name):
        self.name     = name
        self.network  = network 

    def say(self, message):
        message = ':' + message
        self.network.send('PRIVMSG', self.name, message)

class Connection:
    _socket   = None
    _listener = None
    _host     = None
    _port     = 6667

    _ssl      = False
    connected = False
    logger    = None

    def __init__(self, host, port=6667):
        self._host   = host
        self._port   = port

        if self._host.startswith('+'):
            self._host = self._host[1:]
            self._ssl = True

    def connect(self):
        logging.debug('Establishing connection to %s:%s' % (self._host, self._port))
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self._ssl:
            self._socket = ssl.wrap_socket(self._socket)
        try:
            self._socket.connect((socket.gethostbyname(self._host), self._port))

        except socket.error as error:
            logging.warning(error)
            return False

        self.listener = self._socket.makefile('r', 512)

        self.connected = True
        return self.connected

    def send(self, *msg, **kwargs):
        if not self.connected:
            return

        line = ' '.join(msg)

        line += '\r\n'

        line = line.encode('utf-8')

        if len(msg) > 2:
            log_event  = msg[0]
            log_message = ' '.join(msg[1:])

            logging.debug('\033[91m→\033[0m %s %s' % (
              log_event.ljust(8),
              ('"%s"' % log_message if log_message else '' )
            ))

        self._socket.send(line)

    def parse(self, line): return

    def run(self):
        if not self.connected:
            self.connect()

        while self.connected:
            line = self.listener.readline()
            line = line.strip()
            if line:
                response = self.parse(line)
                if response:
                    self.send(response)

class Network(Connection):

    def _null(self, *args, **kwargs):
        return ''

    def got_end_of_motd(self, host, mode, receiver, rest):
        for channel in self.channels:
            self.join(channel)

    def got_names(self, host, mode, receiver, rest):
        channel = self.channel_by_name(rest[1])
        if channel:
            nicknames = rest[3:]

            for nick in nicknames:
                user = self.user_by_nick(nick, create=True)
                self.users.append(user)
                user.channels.append(channel)
                channel.users.append(user)
        return

    def got_privmsg(self, host, mode, receiver, rest):
        user    = self.user_by_host(host)
        message = ' '.join(rest)[1:]

        if receiver.startswith('#'):
            # public msg
            channel = self.channel_by_name(receiver)
            if channel:
                self.message(user, channel, message)
        else:
            # private msg
            if not user:
                user = self.user_by_host(host, create=True)
                self.private_message(user, message)
        return ''

    def got_nick(self, host, mode, receiver, rest):
        user = self.user_by_host(host)
        old_nick = user.nick
        user.nick = receiver[1:]
        for channel in user.channels:
            self.user_rename(user, channel, old_nick)

    def got_join(self, host, mode, receiver, rest):
        user = self.user_by_host(host, create=True)
        channel = self.channel_by_name(receiver)

        self.user_joined(user, channel)

    def got_part(self, host, mode, receiver, rest):
        user = self.user_by_host(host)
        channel = self.channel_by_name(receiver)

        self.user_left(user, channel)

        channel.users.remove(user)
        user.channels.remove(channel)
        
        if not user.channels:
            self.users.remove(user)
            del user

    def got_quit(self, host, mode, receiver, rest):
        user = self.user_by_host(host)

        for channel in user.channels:
            channel.users.remove(user)
            user.channels.remove(channel)
            self.user_quit(user, channel)

        self.users.remove(user)
        del user

    def got_kick(self, host, mode, receiver, rest):
        user = self.user_by_host(host)
        channel = self.channel_by_name(receiver)
        kickee = self.user_by_nick(rest[0])
        reason = rest[1][1:]

        channel.users.remove(user)
        user.channels.remove(channel)

        if not user.channels:
            self.users.remove(user)

        self.user_kicked(self, user, channel, kickee, reason)
        
    def got_topic(self, host, mode, receiver, rest):
        return

    def got_mode(self, host, mode, receiver, rest):
        return

    def __init__(self, host, port, nick, ident = "", realname = "", channels = []):

        self._actions = {
          '353':     self.got_names,
          '376':     self.got_end_of_motd,
          '422':     self.got_end_of_motd,
          'PRIVMSG': self.got_privmsg,
          'NICK':    self.got_nick,
          'JOIN':    self.got_join,
          'PART':    self.got_part,
          'QUIT':    self.got_quit,
          'KICK':    self.got_kick,
          'MODE':    self.got_mode,
        }

        self._host = host
        self._port = port

        if self._host.startswith('+'):
            self._host = self._host[1:]
            self._ssl = True

        self.nick     = nick
        self.ident    = ident    if ident    else self.nick
        self.realname = realname if realname else self.ident

        self.channels = {}
        self.users    = []

        for channel in channels:
            self.channels[channel] = Channel(self, channel)

        self.identify()

    def identify(self):
        logging.debug('Identifying')
        self.connect()
        self.send('USER', self.ident, '8', '*', ':' + self.realname)
        self.send('NICK', self.nick)

    def user_by_nick(self, nick, create=False):
        user = None

        flags = ""

        if create and nick.startswith(_valid_user_flag):
            flags += nick[0]
            nick = nick[1:]

        try:
            nickname = nick.lower()
            user = [u for u in self.users if u.nick.lower() == nickname][0]
        except IndexError:
            if create:
                user = User(self, nick, flags)

        return user

    def user_by_host(self, host, create=False):
        if host.startswith(':'): host = host[1:]

        nick, hostmask = host.split('!')
        ident, host    = hostmask.split('@')

        user = self.user_by_nick(nick, create)

        if user:
            if not user.ident:  user.ident = ident
            if not user.host:   user.host  = host

        return user 

    def parse(self, line):

        if line.startswith('PING'):
            return 'PONG' + line[4:]

        elif line.startswith(':'):
            parts = line[1:].split(' ')

            if len(parts) > 2:
                host, mode, receiver, *rest = parts

                log_message = ' '.join(rest)[1:]

                logging.debug('\033[92m←\033[0m %s "%s" %s' % (
                    mode.ljust(8), receiver, 
                    ('"%s"' % log_message if log_message else '' )
                ))
                self._actions.get(mode, self._null)(host, mode, receiver, rest)
        return 

    def channel_by_name(self, name):
        return self.channels.get(name, None)

    def join(self, channel, password=""):
        self.send('JOIN', channel, password)

    '''
       This is where the magic happends, these do nothing by default
       but can be hooked by scripts
    '''

    @hookable
    def message(self, user, channel, message):
        if message.startswith(config.trigger):
            arguments = ''
            command, *args = message[1:].split(' ', 1)
            if args:
                arguments = args[0]

            if command in doctor.commands:
                try:
                    doctor.commands[command](user, channel, arguments) 
                except BaseException as exc:
                    logging.warning('%s: %s' % (exc.__class__.__name__, exc))
                except:
                    pass
        return

    @hookable
    def private_message(self, user, message): return

    @hookable
    def user_rename(self, user, channel, old_nick): return

    @hookable
    def user_left(self, user, channel): return

    @hookable
    def user_joined(self, user, channel): return

    @hookable
    def user_quit(self, user, channel): return

    @hookable
    def user_kicked(self, kicker, channel, kickee, reason): return

    @hookable
    def topic(self, user, channel, topic): return

    @hookable
    def channel_mode(self, channel, modes): return

    @hookable
    def user_mode(self, user, channel): return
