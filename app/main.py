from app.routers.assess  import content_assessment_router
from fastapi import FastAPI, APIRouter
from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware CORS
import logging
logger = logging.getLogger("uvicorn")


app = FastAPI()

# origins=[
#     "http://localhost:3000",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# setup_db_events(app)
# app.add_event_handler("startup", load_prompts)

app.include_router(content_assessment_router, prefix='/api')