#!/usr/bin/env bash

# model: https://fasttext.cc/docs/en/language-identification.html
wget https://www.dropbox.com/s/yjgm028s4j3rrr6/lid.176.bin?dl=0 -O lid.176.bin
git clone https://github.com/facebookresearch/fastText.git
cd fastText
pip install .