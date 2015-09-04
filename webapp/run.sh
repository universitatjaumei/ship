#!/bin/bash
pushd `dirname $0` > /dev/null

docker rm -f ship-webapp-server

docker build -t ship/webapp-server dockerized-ship-webapp-server

cp -a ../ship  $(pwd)

docker run -d -p 5000:5000 -v /opt/devel/workspaces/uji/ship/webapp:/src --name ship-webapp-server ship/webapp-server

popd > /dev/null
