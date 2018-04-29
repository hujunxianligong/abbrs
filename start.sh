#!/bin/bash
mkdir log
nohup python3 run_gunicorn.py -w 5 -b 0.0.0.0:5007 app:app > log/abb_seg.log 2>&1 &