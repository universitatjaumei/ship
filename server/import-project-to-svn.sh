#!/bin/bash

svn mkdir -m "Import code for project $1" svn://localhost/repos/$1
svn mkdir -m "Import code for project $1" svn://localhost/repos/$1/tags
svn mkdir -m "Import code for project $1" svn://localhost/repos/$1/branches

dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

cd $dir/../code/$2
svn import -m "Import code for project $1" . svn://localhost/repos/$1/trunk
