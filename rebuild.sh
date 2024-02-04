docker container stop famcontrol
docker container rm famcontrol
docker image rm famcontroli
docker build -t famcontroli .
docker run -d --name famcontrol --restart always famcontroli
docker container ls
