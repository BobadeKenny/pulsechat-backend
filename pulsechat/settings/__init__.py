from pulsechat.settings.production import *  

try:
    from pulsechat.settings.local import *  
except ImportError:
    pass
