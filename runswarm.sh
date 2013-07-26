#!/bin/sh

SH_PATH=$(dirname `realpath $0`)

PYTHONPATH=$SH_PATH python $@
