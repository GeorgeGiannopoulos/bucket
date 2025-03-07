# server.py ----------------------------------------------------------------------------------------
#
# Description:
#    This script is the wrapper script of the Bucket like API.
#
# --------------------------------------------------------------------------------------------------


# ==================================================================================================
# Logging
# ==================================================================================================
#
import time
import logging
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO,
                    datefmt="%Y-%m-%dT%H:%M:%S.000Z")
logging.Formatter.converter = time.gmtime
logger = logging.getLogger('bucket')


# ==================================================================================================
# Imports
# ==================================================================================================
# Build-in
# NOTE: Import here the Built-in modules
# Installed
import uvicorn
# Custom
from app.app import create_app
from app.settings import Config


# ==================================================================================================
# Constants
# ==================================================================================================
#
app = create_app()


# ==================================================================================================
# Main
# ==================================================================================================
#
if __name__ == "__main__":
    logger.info('Starting Bucket...')
    uvicorn.run("server:app",
                host="0.0.0.0",
                port=Config.BUCKET_PORT,
                log_level=Config.LOG_LEVEL,
                reload=Config.DEBUG,
                workers=Config.WORKERS)
