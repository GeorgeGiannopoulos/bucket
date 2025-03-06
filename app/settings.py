# settings.py --------------------------------------------------------------------------------------
#
# Description:
#    This script contains the app's settings
#
# --------------------------------------------------------------------------------------------------


# ==================================================================================================
# Imports
# ==================================================================================================
# Build-in
from os import environ, pardir
from os.path import abspath, dirname, join
# Installed
# NOTE: Add here the Installed modules
# Custom
# NOTE: Add here the Custom modules


# ==================================================================================================
# Classes
# ==================================================================================================
#
class ConfigEnv(object):
    """Environmental Configuration"""
    # Execution Mode
    # NOTE: To control execution mode export the OS environmental variable 'EXECUTION_MODE' to
    #       'development' to use the Development mode [default: 'production']
    EXECUTION_MODE = environ.get('EXECUTION_MODE', 'production')
    # Bucket URL
    BUCKET_HOST = environ.get('BUCKET_HOST', 'bucket.domain.gr')
    BUCKET_PORT = int(environ.get('BUCKET_PORT', 8000))
    # Log Level
    LOG_LEVEL = 'info'
    WORKERS = int(environ.get('WORKERS', 4))

    #
    # --- Dev Mode ---
    #
    if EXECUTION_MODE != 'production':
        WORKERS = 1


class ConfigApp(ConfigEnv):
    """Base Configuration"""
    SETTINGS_DIR = abspath(dirname(__file__))  # This directory
    APP_DIR = abspath(join(SETTINGS_DIR))
    PROJECT_ROOT = abspath(join(APP_DIR, pardir))
    FILES_DIR = abspath(join(PROJECT_ROOT, 'files'))

    UTC_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


class ConfigFastAPI(ConfigEnv):
    """Production FastAPI Configuration"""
    ENV = 'prod'
    DEBUG = False
    # Middleware
    CORS_ORIGIN_WHITELIST = [
        f'http://{ConfigEnv.BUCKET_HOST}',
        f'https://{ConfigEnv.BUCKET_HOST}'
        # TODO: Add here all the eligible URL that can access the backend
    ]
    CORS_ALLOW_METHODS = ['*']
    CORS_ALLOW_HEADERS = ['*']
    CORS_EXPOSE_HEADERS = ['Content-Disposition']
    #
    # --- Dev Mode ---
    #
    if ConfigEnv.EXECUTION_MODE != 'production':
        ENV = 'dev'
        DEBUG = True
        # Middleware
        CORS_ORIGIN_WHITELIST = '*'
        CORS_ALLOW_METHODS = ['*']
        CORS_ALLOW_HEADERS = ['*']


class Config(ConfigApp, ConfigFastAPI):
    """All Configuration"""
