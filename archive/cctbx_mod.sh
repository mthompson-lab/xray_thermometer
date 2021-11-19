#!/usr/bin/env bash

py_ver="$(which libtbx.python)"

echo "$py_ver"

# $py_ver -m pip install virtualenv

# mkdir ~/thermometry

# cd ~/thermometry

# virtualenv --version

# virtualenv thermometry

# virtualenv -p "$py_ver" thermometry

# source thermometry/bin/activate

$py_ver -m pip install scipy pandas numpy



