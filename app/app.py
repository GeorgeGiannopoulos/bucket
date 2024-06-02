# app.py -------------------------------------------------------------------------------------------
#
# Description:
#    This script initialize the fastapi app
#
# --------------------------------------------------------------------------------------------------


# ==================================================================================================
# Logging
# ==================================================================================================
#
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)-8s | %(module)-12s | %(lineno)-4d | %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# ==================================================================================================
# Imports
# ==================================================================================================
# Build-in
# NOTE: Add here all the Build-in modules
# Installed
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Custom
from app.settings import Config, ConfigFastAPI
from app import routes


# ==================================================================================================
# Functions
# ==================================================================================================
#
def create_app():
    """Create a FastAPI application."""
    logger.info("Execution mode: '{}'".format(Config.EXECUTION_MODE))
    app = FastAPI()
    app.config = ConfigFastAPI
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ConfigFastAPI.CORS_ORIGIN_WHITELIST,
        allow_credentials=True,
        allow_methods=ConfigFastAPI.CORS_ALLOW_METHODS,
        allow_headers=ConfigFastAPI.CORS_ALLOW_HEADERS,
        expose_headers=["Content-Disposition"],
    )
    app.include_router(routes.router)
    return app
