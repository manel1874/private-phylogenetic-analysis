
from threading import Thread, Event
from flask import Flask, Response, render_template
from flask import request
import json
import os

from flask.views import MethodView


server = Flask(__name__)


@server.route('/file', methods = ['POST'])
def FILE():
    f = request.files['upload_file']
    f.save("Sequences_Received.txt")
    return "FILE TRANSFERED"

@server.route('/fileServer', methods = ['POST'])
def FILESERVER():
    f = request.files['upload_file']
    ip = request.remote_addr
    filename = f.filename
    f.save('../Selected_Sequences/' + filename)
    return "FILE TRANSFERED"
    

if __name__ == '__main__':
    
    configs = open("../config.txt","r")
    ip = configs.readline()
    configs.close()
    ip = ip.split(":")[1].rstrip()
    server.run(host=str(ip), port=8090, debug=True)
    
    
