from common import *

DEPLOYMENT_LEVEL = "hegenv"

#STANDALONE = True
RELOAD_TEMPLATES = True

ALLOWED_HOSTS = ["37.187.98.23","localhost","127.0.0.1"]
injectSecrets(DEPLOYMENT_LEVEL)