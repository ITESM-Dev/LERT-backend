from imp import reload
import os

port = int(os.getenv('PORT', 8000))
bind = f":{port}"
timeout = 1000
loglevel= 'debug'
workers = 2
reload = False