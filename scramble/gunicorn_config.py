
# http://docs.gunicorn.org/en/latest/settings.html

chdir = '/opt/cadizm/lib/scramble/scramble'

bind = '127.0.0.1:5002'
proc_name = 'scramble.wsgi'
pidfile = '/opt/cadizm/var/run/scramble.pid'

import multiprocessing
workers = multiprocessing.cpu_count() * 2 + 1

reload = True
daemon = False  # use systemd
capture_output = True

user = 'www-data'
group = 'www-data'

accesslog = '/opt/cadizm/var/log/scramble-access.log'
errorlog = '/opt/cadizm/var/log/scramble-error.log'
