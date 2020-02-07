import multiprocessing

bind = '0.0.0.0:5001'
worker_class = 'gevent'
workers = multiprocessing.cpu_count() * 2 + 1
loglevel = 'INFO'
errorlog = '-'
accesslog = '-'
timeout = 360
