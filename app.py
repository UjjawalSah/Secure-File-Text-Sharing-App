from flask import Flask, render_template, request, jsonify, send_file, session
import os
import random
import string
import uuid
import mimetypes
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secure secret key
UPLOAD_FOLDER = 'uploads'
TEXT_STORAGE = {}
VISITOR_COUNT_FILE = 'visitor_count.txt'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

limiter = Limiter(get_remote_address, app=app, default_limits=["10 per minute"])

def generate_secure_code():
    return ''.join(random.choices(string.digits, k=4))  # Generate 4-digit code

def allowed_file(filename):
    allowed_extensions = {'txt', 'jpg', 'png', 'pdf', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_visitor_count():
    if not os.path.exists(VISITOR_COUNT_FILE):
        with open(VISITOR_COUNT_FILE, 'w') as f:
            f.write('0')
    with open(VISITOR_COUNT_FILE, 'r') as f:
        return int(f.read().strip())

def increment_visitor_count():
    count = get_visitor_count() + 1
    with open(VISITOR_COUNT_FILE, 'w') as f:
        f.write(str(count))
    return count

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/upload', methods=['POST'])
@limiter.limit("5 per minute")
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': 'Invalid file type'}), 400
    
    file_code = generate_secure_code()
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, file_code + '_' + filename)
    file.save(file_path)
    
    return jsonify({'status': 'success', 'message': 'File uploaded successfully', 'fileCode': file_code})

@app.route('/retrieve', methods=['GET'])
@limiter.limit("10 per minute")
def retrieve_file():
    file_code = request.args.get('fileCode')
    if not file_code:
        return jsonify({'status': 'error', 'message': 'No file code provided'}), 400
    
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.startswith(file_code + '_'):
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            return send_file(file_path, as_attachment=True)
    
    if file_code in TEXT_STORAGE:
        text_content = TEXT_STORAGE[file_code]
        text_file_path = os.path.join(UPLOAD_FOLDER, file_code + '_text.txt')
        with open(text_file_path, 'w') as text_file:
            text_file.write(text_content)
        return send_file(text_file_path, as_attachment=True)
    
    return jsonify({'status': 'error', 'message': 'File or text not found'}), 404

@app.route('/share', methods=['POST'])
@limiter.limit("5 per minute")
def share_text():
    text = request.form.get('sharedText')
    if not text:
        return jsonify({'status': 'error', 'message': 'No text provided'}), 400
    
    text_code = generate_secure_code()
    TEXT_STORAGE[text_code] = text
    
    return jsonify({'status': 'success', 'message': 'Text shared successfully', 'textCode': text_code})

@app.route('/visitor-count')
def visitor_count_endpoint():
    if 'visited' not in session:
        session['visited'] = True
        count = increment_visitor_count()
    else:
        count = get_visitor_count()
    return jsonify(count)

 
