# routes.py ----------------------------------------------------------------------------------------
#
# Description:
#    This script contains all the routes regarding files
#
# --------------------------------------------------------------------------------------------------


# ==================================================================================================
# Routes table of contents
# ==================================================================================================
# Search the Routes based on the following patterns (comments)
#
# | Pattern             | URL                        | Methods | Comments
# |---------------------|----------------------------|---------|------------------------------------
# | --- (router 01) --- | /                          | GET     | Return a JSON to ensure that the REST-API is alive
# | --- (router 02) --- | /bucket/v1/file            | POST    | Stores a file to the Bucket
# | --- (router 03) --- | /bucket/v1/file/{filename} | PUT     | Updates a file to the Bucket
# | --- (router 04) --- | /bucket/v1/file/{filename} | GET     | Returns a file from the Bucket
# | --- (router 05) --- | /bucket/v1/file/{filename} | DELETE  | Deletes a file from the Bucket


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
# Installed
from fastapi import APIRouter
from fastapi import File, UploadFile, HTTPException, Response
# Custom
from app.models import Metadata
from app.utilities import file_name, file_path, file_exists, remove_from_bucket, file_from_bucket, \
    unique_filename, file_to_bucket, file_metadata


# ==================================================================================================
# Constants
# ==================================================================================================
#
router = APIRouter()


# ==================================================================================================
# Main
# ==================================================================================================
#
# --- (router 01) ---
@router.get('/', tags=['health'], status_code=200)
async def api_is_alive():
    """This endpoint returns OK to ensure the Bucket is up and running"""
    return {'message': 'The Bucket is up and running'}


# --- (router 02) ---
@router.post('/bucket/v1/file', tags=['bucket'], response_model=Metadata | str)
async def upload_file(file: UploadFile = File(...), unique: bool = False, metadata: bool = False):
    """This endpoint stores a file in the Bucket"""
    filename = unique_filename(file) if unique else file_name(file)
    if filename == '':
        raise HTTPException(status_code=400, detail="No file uploaded!")
    filepath = file_path(filename)
    if file_exists(filepath):
        raise HTTPException(status_code=409, detail=f"File {filename} already exists!")
    try:
        file_to_bucket(file, filepath)
        return file_metadata(file, filename) if metadata else filename
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=f"Failed to store file {filename}!")


# --- (router 03) ---
@router.put('/bucket/v1/file/{filename}', tags=['bucket'], response_model=Metadata | str)
async def update_file(filename: str, file: UploadFile = File(...), metadata: bool = False):
    """This endpoint updates a file in the Bucket"""
    filepath = file_path(filename)
    if not file_exists(filepath):
        raise HTTPException(status_code=404, detail=f"File {filename} not found!")
    try:
        file_to_bucket(file, filepath)
        return file_metadata(file, filename) if metadata else filename
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=f"Failed to updated file {filename}!")


# --- (router 04) ---
@router.get('/bucket/v1/file/{filename}', tags=['bucket'])
async def get_file(filename: str):
    """This endpoint returns a file from the filesystem"""
    filepath = file_path(filename)
    if not file_exists(filepath):
        raise HTTPException(status_code=404, detail=f"File {filename} not found")
    file_content = file_from_bucket(filepath)
    return Response(content=file_content, media_type="application/octet-stream", headers={"Content-Disposition": f"attachment; filename={filename}"})


# --- (router 05) ---
@router.delete("/bucket/v1/file/{filename}", tags=['bucket'])
async def delete_file(filename: str):
    """This endpoint deletes a file from the filesystem"""
    filepath = file_path(filename)
    if not file_exists(filepath):
        raise HTTPException(status_code=404, detail=f"File {filename} not found!")
    remove_from_bucket(filepath)
    return {"message": f"File {filename} deleted successfully"}
