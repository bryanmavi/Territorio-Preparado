#!/bin/sh
set -eu
python /opt/xview/xview_runner.py --source /opt/xview/source --pre "$1" --post "$2" --output "$4"
cp "$4" "$3"
