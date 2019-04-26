#!/bin/sh
DIMENSIONS=$(xdpyinfo | grep dimensions | sed -r 's/^[^0-9]*([0-9]+x[0-9]+).*$/\1/')
WIDTH=$(echo $DIMENSIONS | sed -r 's/x.*//')
HEIGHT=$(echo $DIMENSIONS | sed -r 's/.*x//')
python2 paint.py $WIDTH $HEIGHT $1 $2 $3 $4 $5
