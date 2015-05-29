#!/bin/bash

fab --user "aplicacions" --hosts "devel01.uji.es" deploy:app="sample",home="/tmp/tomcat",user="tomcat",password="tomcat"
