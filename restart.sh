docker kill xblock-sdk && docker rm xblock-sdk
docker build . -t xblock
docker run -d -p 8000:8000 --name xblock-sdk xblock
