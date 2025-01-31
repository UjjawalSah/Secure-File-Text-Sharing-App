from flask import Flask, render_template, request, jsonify, send_file, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import random
import threading

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'supersecretkey')  # Use a fixed key for session persistence

# Use /tmp for storage
UPLOAD_FOLDER = '/tmp/uploads'
TEXT_STORAGE = {}
USED_CODES = set()
LOCK = threading.Lock()  # Thread safety for TEXT_STORAGE
VISITOR_COUNT_FILE = '/tmp/visitor_count.txt'

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Flask Limiter for rate limiting
limiter = Limiter(app, key_func=get_remote_address, default_limits=["10 per minute"])

def generate_unique_code():
    """Generate a unique 4-digit code."""
    while True:
        code = str(random.randint(1000, 9999))  # Generate a 4-digit number
        with LOCK:
            if code not in USED_CODES:
                USED_CODES.add(code)
                return code

def allowed_file(filename):
    """Check if the file extension is allowed."""
    allowed_extensions = {'txt', 'jpg', 'png', 'pdf', 'docx'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/upload', methods=['POST'])
@limiter.limit("5 per minute")
def upload_file():
    """Handles file uploads securely."""
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'status': 'error', 'message': 'Invalid file type'}), 400
    
    file_code = generate_unique_code()
    filename = f"{file_code}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    try:
        file.save(file_path)
        return jsonify({'status': 'success', 'message': 'File uploaded successfully', 'fileCode': file_code})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/retrieve', methods=['GET'])
@limiter.limit("10 per minute")
def retrieve_file():
    """Handles file retrieval based on a given file code."""
    file_code = request.args.get('fileCode')
    if not file_code:
        return jsonify({'status': 'error', 'message': 'No file code provided'}), 400
    
    try:
        for filename in os.listdir(UPLOAD_FOLDER):
            if filename.startswith(file_code + '_'):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                return send_file(file_path, as_attachment=True)

        # Retrieve shared text if no file is found
        with LOCK:
            if file_code in TEXT_STORAGE:
                text_content = TEXT_STORAGE[file_code]
                text_file_path = os.path.join(UPLOAD_FOLDER, file_code + '_text.txt')
                with open(text_file_path, 'w') as text_file:
                    text_file.write(text_content)
                return send_file(text_file_path, as_attachment=True)
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'error', 'message': 'File or text not found'}), 404

@app.route('/share', methods=['POST'])
@limiter.limit("5 per minute")
def share_text():
    """Stores and shares text content using a unique 4-digit code."""
    text = request.form.get('sharedText')
    if not text:
        return jsonify({'status': 'error', 'message': 'No text provided'}), 400
    
    text_code = generate_unique_code()
    with LOCK:
        TEXT_STORAGE[text_code] = text

    return jsonify({'status': 'success', 'message': 'Text shared successfully', 'textCode': text_code})

if __name__ == '__main__':
    app.run(debug=True)
