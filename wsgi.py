import sys
from os.path import abspath
from os.path import dirname
import app


sys.path.insert(0, abspath(dirname(__file__)))
application = app.app

"""
➜  ~ cat /etc/supervisor/conf.d/bbs.conf

[program:bbs]
command=/usr/local/bin/gunicorn wsgi -c /usr/local/bin/gunicorn wsgi --bind 0.0.0.0:2001 --pid /tmp/bbs.pid
directory=/var/www/bbs
autostart=true
autorestart=true




/usr/local/bin/gunicorn wsgi
--bind 0.0.0.0:2001
--pid /tmp/blog.pid
"""
