from imp import reload
import os

if os.getenv('ENVIRONMENT') == 'dev':
    bind = ":8000"
    timeout = 1000
    loglevel= 'debug'
    workers = 1
    reload = True
elif os.getenv('ENVIRONMENT') == 'prod':
    port = int(os.getenv('PORT', 8000))
    bind = f":{port}"
    timeout = 1000
    loglevel= 'debug'
    workers = 2
    reload = False