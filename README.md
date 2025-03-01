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


# download_rename.py
Its function is downloading the data we used into ./evaluation/dataset

This involves download-unzip-rename-move. 


# gen_ground_truth.py
Its function is generating ground truth. This is realized through hard coding.

The ground truth is a table. 

The 1st column 'video_id' is file name. File type can be .mp4 or .avi. 

The 2nd column 'is_violence' is whether it involves violence, 1 for yes 0 for no. 

The 3rd column 'detection result' is our model's judgement of whether this video involves violence, 1 for yes 0 for 0. 

The 4th to 7th columns are whether this sample is true positive or true negative or false negative or false positive. 
