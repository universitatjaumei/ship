docker kill $(docker ps -q)
docker rm $(docker ps -a -q)

docker run -p 8080:80 -v /home/borillo/Descargas:/usr/share/nginx/html:ro -d nginx

docker build -t ship/deploy-server .

docker run -d -p 2222:22 -p 8888:8080 ship/deploy-server
docker run -e SVN_REPONAME=repos -p 3690:3690 -d erikxiv/subversion

sleep 1

../import-project-to-svn.sh SAMPLE sample
../import-project-to-svn.sh SAMPLE-MULTIMODULE sample-multimodule