import multiprocessing

bind = '0.0.0.0:5000'
workers = multiprocessing.cpu_count() * 2 + 1
loglevel = 'INFO'
errorlog = '-'
accesslog = '-'
timeout = 120
