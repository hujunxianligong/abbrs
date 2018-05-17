#!/bin/bash

kill -9 `ps -ef | grep 'app:app load_seg' | awk '{print $2}'`