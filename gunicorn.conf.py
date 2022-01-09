import multiprocessing

from gevent import monkey

monkey.patch_all()
debug = False
loglevel = 'debug'
bind = '0.0.0.0:1228'
daemon = False
reload = True
pidfile = 'log/gunicorn.pid'
logfile = 'log/debug.log'
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'gevent'
