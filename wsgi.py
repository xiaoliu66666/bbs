import sys
from os.path import abspath
from os.path import dirname
import app


sys.path.insert(0, abspath(dirname(__file__)))
application = app.app

"""
建立一个软连接（右边指向左边）
ln -s /var/www/bbs/bbs.conf /etc/supervisor/conf.d/bbs.conf

➜  ~ cat /etc/supervisor/conf.d/bbs.conf

[program:bbs]
command=/usr/local/bin/gunicorn wsgi -c gunicorn_conf.py
directory=/var/www/bbs
autostart=true
autorestart=true




/usr/local/bin/gunicorn wsgi
--bind 0.0.0.0:2001
--pid /tmp/blog.pid
"""
