docker rm -f ship-deploy-server
docker rm -f ship-svn

docker build -t ship/deploy-server .

docker run -d -p 2222:22 -p 8888:8080 --name ship-deploy-server ship/deploy-server
docker run -e SVN_REPONAME=repos -p 3690:3690 -d --name ship-svn erikxiv/subversion

sleep 1

./import-project-to-svn.sh SAMPLE sample
./import-project-to-svn.sh SAMPLE-MULTIMODULE sample-multimodule
