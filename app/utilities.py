# utilities.py -------------------------------------------------------------------------------------
#
# Description:
#    This script contains utilities
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
import os
import hashlib
import datetime
# Installed
from fastapi import UploadFile
# Custom
from app.settings import Config
from app.models import Metadata


# ==================================================================================================
# Functions
# ==================================================================================================
#
def file_name(file: UploadFile):
    """This function returns the file's path"""
    return file.filename


def file_path(filename: str):
    """This function returns the file's path"""
    return os.path.join(Config.FILES_DIR, filename)


def file_exists(filepath: str):
    return os.path.exists(filepath)


def file_to_bucket(file: UploadFile, filepath: str):
    """This function writes a file to the Bucket"""
    with open(filepath, "wb") as f:
        f.write(file.file.read())


def file_from_bucket(filepath: str):
    """This function reads a file from the Bucket"""
    with open(filepath, "rb") as f:
        return f.read()


def remove_from_bucket(filepath: str):
    """This function removes a file from the Bucket"""
    os.remove(filepath)


def now():
    """This function returns the current timestamp"""
    return datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')


def file_extension(file: UploadFile):
    """This function returns a file's extension"""
    fn, ext = os.path.basename(file_name(file)).split('.')
    return ext


def file_to_blob(file: UploadFile):
    """This function reads a file and resets the pointer to the beginning"""
    blob = file.file.read()
    file.file.seek(0)  # Reset the file pointer to the beginning
    return blob


def file_size(file: UploadFile):
    """This function returns the file's size"""
    return os.path.getsize(file_path(file_name(file)))


def file_hash(file: UploadFile):
    """This function returns a hash calculated using the file content"""
    return hashlib.sha256(file_to_blob(file)).hexdigest()


def unique_filename(file: UploadFile):
    """This function returns a unique filename"""
    return f"{file_hash(file)}.{now()}.{file_extension(file)}"


def file_metadata(file: UploadFile, saved_as: str):
    """This function returns the file's metadata"""
    return Metadata(original=file.filename,
                    saved_as=saved_as,
                    type=file.content_type,
                    size=file_size(file))
