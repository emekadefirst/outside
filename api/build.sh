#!/bin/bash

openssl rand -hex 32

pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8000

docker build -t server .
docker run -p 8000:8000 server

