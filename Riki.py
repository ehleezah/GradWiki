#!/Users/smcho/virtualenv/riki/bin/python

# -*- coding: utf-8 -*-
import os

from wiki import create_app


directory = os.getcwd()
app = create_app(directory)

if __name__ == '__main__':
    app.run(host='localhost',port=5000, debug=True)
