#!/usr/bin/env bash

# model: https://fasttext.cc/docs/en/language-identification.html
wget https://www.dropbox.com/s/yjgm028s4j3rrr6/lid.176.bin?dl=0 -O lid.176.bin
pip install pybind11
pip install fasttext-wheel
