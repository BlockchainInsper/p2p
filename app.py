
from flask import Flask, jsonify, request
import hashlib
from os import listdir
from os.path import isfile, join

BUF_SIZE = 65536

app = Flask(__name__) 


  
@app.route('/files', methods=['GET']) 
def hello_world(): 
    path = "./files"
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    resp = []

    sha256 = hashlib.sha256()
    
    for current_file in onlyfiles:
    
        with open(path + "/" + current_file,'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha256.update(data)
            resp.append({'name':current_file, 'hash':sha256.hexdigest()})
    return jsonify({'status':'success', 'data':resp})



@app.route('/files', methods=['POST']) 
def recive_file(): 
    try:
        file_uploaded = request.files['file']
    except:
        file_uploaded = None
        return jsonify({'status':'fail', 'data':'missing file'})
    file_uploaded.save("./files/" + file_uploaded.filename)
    return jsonify({'status':'success', 'data':{'filename': file_uploaded.filename}})


  
if __name__ == '__main__': 

    app.run() 


