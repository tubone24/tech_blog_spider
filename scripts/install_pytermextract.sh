#!/usr/bin/env bash

# Source http://gensen.dl.itc.u-tokyo.ac.jp/pytermextract/
wget https://www.dropbox.com/s/8l6ufugc7n99l9w/pytermextract-0_01.zip?dl=0 -O open_file.zip
unzip open_file.zip
cd pytermextract-0_01
python setup.py install