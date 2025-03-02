from ..utils.video_processor import framming
from fastapi.responses import JSONResponse
import uuid
import logging
from volcenginesdkarkruntime import Ark
from fastapi import APIRouter, Request, UploadFile, File, Depends, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
import logging
from app.utils.tos import upload_frames
from app.recognition.llm import image2text,get_ark_client,check_violence

logger = logging.getLogger("uvicorn")


content_assessment_router = APIRouter()
DATA_DIR = '/data'
UPLOAD_DIR = 'raw'
PROCESS_DIR = 'process'


@content_assessment_router.api_route(
    "/assess", methods=["POST"]
)
async def assess(request: Request, file: UploadFile = File(None), client: Ark = Depends(get_ark_client)):
    """content assessment"""
    if request.headers.get('API_KEY') != os.getenv('REVELIO_API_KEY'):
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")

    if not file:
        return JSONResponse(content={'message': 'file upload failed'}, status_code=500)
    else:
        file_uuid = uuid.uuid4().__str__()

        stored_dir_path = Path(DATA_DIR) / Path(UPLOAD_DIR) / Path(file_uuid)
        stored_dir_path.mkdir()
        file_path = stored_dir_path / Path(file.filename)

        with open(file_path, "wb") as f:
            contents = await file.read()
            f.write(contents)

        frame_dir = Path(DATA_DIR) / Path(PROCESS_DIR) / Path(file_uuid)
        frame_dir.mkdir()
        output_pattern = frame_dir / Path('%04d.png')

        file_list = framming(1, file_path, output_pattern)
        name_url = upload_frames(file_uuid, file_list)

        # Detect image with LLM
        serial_result = {}
        for name, url in name_url.items():
            # serial_text[name] = image2text(url, client)
            serial_result[name] = check_violence(url, client)

        return JSONResponse(content=serial_result, status_code=200)