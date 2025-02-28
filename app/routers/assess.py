from fastapi.responses import JSONResponse
import json
import uuid
import logging
import asyncio
from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import JSONResponse
from pathlib import Path
import os
# from zhipuai import ZhipuAI

content_assessment_router = APIRouter()
UPLOAD_DIR = '/data'


@content_assessment_router.api_route(
    "/assess", methods=["POST"]
)
async def assess(request: Request, file: UploadFile = File(None)):
    """content assessment"""
    if file:
        file_uuid = uuid.uuid4().__str__()

        dir_path = Path(UPLOAD_DIR) / Path(file_uuid)
        dir_path.mkdir()
        file_path = dir_path / Path(file.filename)

        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)
        return JSONResponse(content={'message': 'upload success', 'path': file_path.__str__()}, status_code=200)
    else:
        return JSONResponse(content={'message': 'file upload failed'}, status_code=500)

    # identifying by AI
    # risk = True
    # if risk:
    #     return JSONResponse(content={'risk': True, 'category': 'Violence'}, status_code=200)
    # return JSONResponse(content="", status_code=200)
