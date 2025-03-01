# Revelio

A content moderation system powered by AI.

## Usage

### Deployment

1. Build the image from Dockerfile: `docker build -t revelio .`
2. Running a container from image: `docker run -d -p 8000:8000  revelio`

### Interacting

Make request to assessment end point: <http://localhost:8000/api/assess>.

Test with curl: `curl -X 'POST' http://localhost:8000/api/assess  -H 'Content-Type: multipart/form-data' -F 'file=@WRITE_FILE_PATH_HERE'`

## Architecture

- Data Processing:
  - framing video
  - extract sound track from video
- Backend(RESTFul API): FastAPI(Python)
- Recognition:
  - classical neural network
  - large language model

### Process

#### Data Processing

#### Recognition
