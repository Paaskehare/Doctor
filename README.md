This is a Python 3 IRC Bot, it is not meant to have an especially pretty syntax.
But is instead focusing on pretty and functional scripting support. 

An easily extensible IRC Bot written in Python 3
- based on the py3 branch of [python-irclib](https://github.com/farces/python-irclib/tree/py3)

The "Plugin Manager" enables you to load, reload and unload plugins on the fly as the bot is running, simply write:
`.load example` to the bot, and it will load `example.py` in the *scripts* directory.

`.unload` and `.reload` should be self-explanatory



*Requirements:*

- Python 3.x → http://python.org

*Features:*

- Plugin Support (loading/reloading during runtime)
