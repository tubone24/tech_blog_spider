#!/usr/bin/env bash

wget https://www.dropbox.com/s/vai7iasou3nlv50/open_file.zip?dl=0 -O open_file.zip
unzip open_file.zip
cd open_file
python setup.py install