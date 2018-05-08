#!/bin/bash
mkdir log
nohup python3 run_gunicorn.py -w 1 -b 0.0.0.0:5007 app:app 'load_seg --path /mnt/vol_0nd/usr/cmb_in/模型文件/crf_model_30_18050611' > log/abb_seg.log 2>&1 &