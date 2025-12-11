A simple base project represented as an user profile with its own objects (resumes) with enought functionalities.


**How to build**

Frontend:

1. cd frontend
2. docker build -f Dockerfile.frontend .

**How to run**

Frontend:

1. cd frontend
2. docker images
3. From output command above copy id related to the last created image
2. docker run -d -p 9000:82 --name frontend YOUR_IMAGE_ID

Backend:

1. docker compose up -d --build