#!/bin/bash
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
mkdir data
cd data
mkdir text_files
mkdir voice
cd ..
docker build $SCRIPTPATH -t savior
docker run --name saviord -d -v $SCRIPTPATH/data:/data:rw savior
