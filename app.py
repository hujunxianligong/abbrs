# -*- coding: UTF-8 -*-
import os
import re
import sys
from flask import Flask
from flask import request
from load.load_model import get_model_abbr
import config as sys_config

app = Flask(__name__)

@app.route('/api/abbner', methods=['POST'])
def abb_classify():
    data = request.data
    if data == b'':
        data = dict(request.form)
        for key in data:
            data = key
            break
        print(data)
        data = re.sub('[\(（）\)]', '', data)
    else:
        data = re.sub('[\(（）\)]', '', data.decode('UTF-8'))
    result = get_model_abbr(data)
    json = result.set_api_json()
    del result
    return json

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except ValueError and IndexError:
        port = 5007

    while True:
        try:
            app.run(debug=sys_config.DEBUG,host='0.0.0.0', port=port, threaded=False)
        except Exception as e:
            print(e)