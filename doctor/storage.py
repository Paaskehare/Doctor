#!/usr/bin/env python

import os, json

class Storage(object):

    def __init__(self, script):
        self.__dict__['storage'] = {}
        self.__dict__['script']  = script
        self._read_file()

    def __repr__(self):
        return self.__dict__['storage']

    def __setattr__(self, attr, arg):
        self.__dict__['storage'][attr] = arg

    def __getattr__(self, attr):
        return self.__dict__['storage'].get(attr, '')

    def __delattr__(self, attr):
        item = self.__dict__['storage'].get(attr, '')
        if item:
            del self.__dict__['storage'][attr]

    '''
       Store on filesystem
    '''

    def _path(self):
        full_path = os.path.join(os.getcwd(), 'storage')

        return full_path, os.path.join(full_path, self.__dict__['script'] + '.json')

    def _read_file(self):
        p, f = self._path()
        if os.path.exists(p):
            with open(f) as fo:
                self.__dict__['storage'] = json.loads(fo.read())

    def _write_file(self):
        # Only write the file if it contains anything
        print('Writing storage file')
        if self.__dict__['storage']:
            output = json.dumps(self.__dict__['storage'], indent=4)
            p, f = self._path()
            print(p)

            if not os.path.exists(p): os.mkdir(p)
            with open(f, 'w') as fo:
                fo.write(output)
