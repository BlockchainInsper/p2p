
from flask import Flask, jsonify
import hashlib

files = ["bananinha quando nasce", "banana banana"]

app = Flask(__name__) 
  
@app.route('/files') 
def hello_world(): 
    return jsonify({'status':'success', 'data':[hashlib.sha256(i.encode('UTF-8')).hexdigest() for i in files]})
  
if __name__ == '__main__': 

    app.run() 


