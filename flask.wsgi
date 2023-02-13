import sys
sys.path.insert(0,'/var/www/pia-lara')
from pialara import create_app
application = create_app()