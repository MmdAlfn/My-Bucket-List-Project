from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://Alfian:malfian30@ac-a5cun4x-shard-00-00.evy3rrh.mongodb.net:27017,ac-a5cun4x-shard-00-01.evy3rrh.mongodb.net:27017,ac-a5cun4x-shard-00-02.evy3rrh.mongodb.net:27017/?ssl=true&replicaSet=atlas-vpkaxn-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    count = db.bucket.count_documents({})
    num = count + 1
    doc = {
        'num': num,
        'bucket': bucket_receive,
        'done': 0
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg': 'Bucket List baru berhasil disimpan!'})

@app.route("/delete", methods=["POST"])
def delete_bucket():
    num_receive = request.form['num_give']
    db.bucket.delete_one({ 'num': int(num_receive) })
    return jsonify({'msg': 'List berhasil dihapus!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    db.bucket.update_one(
        { 'num': int(num_receive) },
        { '$set': { 'done': 1 } }
    )
    return jsonify({'msg': 'Update berhasil!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': buckets_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)