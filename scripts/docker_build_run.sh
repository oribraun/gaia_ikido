docker stop ikido_classifier
docker rm ikido_classifier
docker build -t ikido_classifier .
# for building locally using sso .aws login folder
# docker build --build-arg AWS_CONFIG_FOLDER=/.aws --build-arg AWS_TARGET_FOLDER=/app/.aws --build-arg AWS_PROFILE=your_profile -t ikido_classifier .
docker run --name ikido_classifier -dp 8080:8080 ikido_classifier
# docker run --name ikido_classifier -dp 8080:8080 ikido_classifier -e ENV=stg
#debug - docker run -it -p 8080:8080 ikido_classifier
