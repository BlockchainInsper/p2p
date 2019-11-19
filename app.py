
from flask import Flask, jsonify, request, send_file
import hashlib
from os import listdir
from os.path import isfile, join
import requests

BUF_SIZE = 65536

app = Flask(__name__) 


  
nodes = []

global hashes
hashes = []



def add_new_node(ip):
    global nodes
    if ip not in nodes and ip not in ["127.0.0.1", "0.0.0.0", "localhost"]:
        nodes.append(ip)







def calculate_all_files_hashes(path):
    global hashes
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

    hashes = resp


def calculate_file_hashe(file_name):
    global hashes

    sha256 = hashlib.sha256()

    
    with open("./files/" + file_name,'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha256.update(data)


    

    return {'name':file_name, 'hash':sha256.hexdigest()}

def get_file_by_hash(hash_number):
    hash_list = [i['hash'] for i in hashes]
    

    index = hash_list.index(hash_number)
    if (index == -1):
        return -1
    else:
        return (hashes[index]['name'])





@app.route('/files', methods=['GET']) 
def add_actual_node():
    ip = request.remote_addr
    add_new_node(ip) 
    global hashes
    return jsonify({'status': 'success', 'data': hashes})

@app.route('/files/<hash>', methods=['GET']) 
def receive_file(hash): 
    global hashes
    file_name = get_file_by_hash(hash)
    if (file_name == -1):
        return ({'status': 'error', 'data': 'hash not found'})
    else:
        return send_file("./files/" + file_name)



@app.route('/files', methods=['POST'])   
def recive_file(): 
    global hashes
    try:
        file_uploaded = request.files['file']
    except:
        file_uploaded = None
        return jsonify({'status':'fail', 'data':'missing file'})
    file_uploaded.save("./files/" + file_uploaded.filename)
    hashes.append(calculate_file_hashe(file_uploaded.filename))
    for i in nodes:
        files = {'upload_file': open("./files/" + file_uploaded.filename,'rb')}
        r = requests.post(i, files=files)

    return jsonify({'status':'success', 'data':{'filename': file_uploaded.filename}})




@app.route('/discovery', methods=['POST']) 
def new_node(): #TODO get files when post
    try:
        action = request.args.get('action')
        ip = request.remote_addr
    except:
        action = None
        return jsonify({'status':'fail', 'data':'missing action'})
    if (action == "add"):
        if (ip not in nodes):
            nodes.append(ip)
        else:
            jsonify({'status':'error', 'data':'already a node'})
    else:
        return jsonify({'status':'error', 'data':'unknown action'})

@app.route('/discovery', methods=['GET'])
def find_node():
    ip = request.remote_addr
    add_new_node(ip) 
    print(ip)
    return jsonify({'status':'success', 'data':[str(i) for i in nodes]})


    


    


  
if __name__ == '__main__': 
    calculate_all_files_hashes("./files")
    app.run(host = "0.0.0.0") 



