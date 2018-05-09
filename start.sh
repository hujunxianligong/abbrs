#!/bin/bash
if [ ! -d "log/" ];then
mkdir log
fi
nohup python3 run_gunicorn.py -w 5 -b 0.0.0.0:5007 app:app 'load_seg ' > log/abb_seg.log 2>&1 &