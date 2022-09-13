import multiprocessing

# http://docs.gunicorn.org/en/latest/settings.html
bind = '0.0.0.0:9002'
workers = multiprocessing.cpu_count() * 2 + 1
reload = True
