# models.py ----------------------------------------------------------------------------------------
#
# Description:
#    This script contains the models' schema
#
# --------------------------------------------------------------------------------------------------


# ==================================================================================================
# Logging
# ==================================================================================================
#
import logging
logger = logging.getLogger(__name__)


# ==================================================================================================
# Imports
# ==================================================================================================
# Build-in
from typing import Optional
from datetime import datetime
# Installed
from pydantic import BaseModel, field_serializer
# Custom
from app.settings import Config


# ==================================================================================================
# Classes
# ==================================================================================================
#
class Metadata(BaseModel):
    original: str
    saved_as: str
    type: str | None
    sha256: str | None
    size: int
    modified_time: Optional[datetime] = None

    @field_serializer('modified_time')
    def serialize_modified_time(self, modified_time: datetime):
        return modified_time.strftime(Config.UTC_FORMAT) if modified_time else modified_time
