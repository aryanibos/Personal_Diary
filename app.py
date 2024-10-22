import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary(): 
    # Mengambil semua data dari koleksi MongoDB
    articles = list(db.diary.find({}, {'_id': False}))  # Mengambil semua tanpa id
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    
    # untuk melihat file yang diupload
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    
    # membuat nama file yang unik
    today = datetime.now()
    date_time = today.strftime("%Y-%m-%d-%H-%M-%S")
    filename = f'static/post-{date_time}.{extension}'
    file.save(filename)
    
    # Mengolah gambar profil
    profile_file = request.files['profile_give']
    profile_extension = profile_file.filename.split('.')[-1]
    profile_filename = f'static/profile-{date_time}.{profile_extension}'
    profile_file.save(profile_filename)
    
    # Posted on tanggal, bulan, tahun
    posted_on = today.strftime("%d %B %Y")
        
    # Membuat format data untuk disimpan
    article = {
        'file': filename,
        'profile': profile_filename,
        'title': title_receive,
        'content': content_receive,
        'posted_on': posted_on
    }
    
    # Menyimpan data ke MongoDB
    db.diary.insert_one(article)
    
    return jsonify({'msg': 'POST request complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
