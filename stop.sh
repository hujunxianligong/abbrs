#!/bin/bash

kill -9 `ps -ef | grep 'run_gunicorn.py -w 5 -b 0.0.0.0:5007' | awk '{print $1}'`