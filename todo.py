from flask import Flask, render_template, request, redirect, url_for
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("C:\\Users\\aamss_9izqos3\\OneDrive\\Desktop\\kontak\\projek-keren-ti-firebase-adminsdk-2r93p-20da6ae733.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route('/')
def index():
    # Baca data dari Firestore
    catatan = baca_data_dari_firestore()
    return render_template('index.html', catatan=catatan)

@app.route('/tambah', methods=['POST'])
def tambah():
    catatan = request.form['catatan']
    if catatan:
        # Simpan data ke dalam Firestore
        catatan_ref = db.collection('catatan')
        catatan_ref.add({'text': catatan})
    return redirect(url_for('index'))

@app.route('/hapus/<int:index>', methods=['POST'])
def hapus(index):
    if request.method == 'POST':
        # Hapus catatan dari Firestore berdasarkan indeks
        catatan_ref = db.collection('catatan')
        catatan = catatan_ref.stream()
        doc_to_delete = None
        for i, doc in enumerate(catatan):
            if i == index:
                doc_to_delete = doc
                break
        if doc_to_delete:
            doc_to_delete.reference.delete()
        return redirect(url_for('index'))

def baca_data_dari_firestore():
    catatan_ref = db.collection('catatan')
    catatan = []
    for doc in catatan_ref.stream():
        catatan_data = doc.to_dict()
        catatan.append(catatan_data['text'])
    return catatan

if __name__ == '__main__':
    app.run(debug=True)
