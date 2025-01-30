# Secure File & Text Sharing App

A secure and simple web application for sharing files and text with unique access codes. The app ensures secure handling, rate limiting, and visitor count tracking.

## Features

- **Secure File Upload & Retrieval**: Users can upload files and retrieve them using a unique 4-digit access code.
- **Text Sharing & Download**: Share text securely and retrieve it as a downloadable text file.
- **File Type Restrictions**: Supports TXT, JPG, PNG, PDF, and DOCX files, preventing unauthorized file types.
- **Visitor Count Tracking**: Persistent visitor count tracking across sessions.
- **Rate Limiting**: Prevents excessive requests to enhance security.

## Technologies Used

- **Flask**: Python web framework for backend functionality.
- **HTML/CSS**: For basic frontend interface.
- **Session Management**: Ensures visitor count persistence.
- **Flask-Limiter**: Protects against abuse with request rate limiting.
- **Werkzeug Secure Filename**: Prevents security vulnerabilities in file handling.

## Installation & Setup

```
# Clone the repository
git clone https://github.com/yourusername/secure-file-sharing.git
cd secure-file-sharing

# Set up a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py

# Access the web app in your browser
http://127.0.0.1:5000/
```

## API Endpoints

1. **Upload File**  
   **Method**: POST  
   **Endpoint**: `/upload`  
   **Request**: Multipart form with a file  
   **Response**: JSON with file access code

2. **Retrieve File/Text**  
   **Method**: GET  
   **Endpoint**: `/retrieve?fileCode={code}`  
   **Response**: Download file or JSON response for text

3. **Share Text**  
   **Method**: POST  
   **Endpoint**: `/share`  
   **Request**: Form data with `sharedText`  
   **Response**: JSON with text access code

4. **Visitor Count**  
   **Method**: GET  
   **Endpoint**: `/visitor-count`  
   **Response**: JSON with visitor count

## Security Measures

- **Restricted File Types**: Only allows specific formats (TXT, JPG, PNG, PDF, DOCX)
- **Rate Limiting**: Limits API requests per user to prevent abuse
- **Session-Based Visitor Counting**: Prevents count increase on refresh
- **Secure File Handling**: Uses `secure_filename()` to avoid path traversal attacks

## Future Enhancements

- Add authentication for restricted access
- Implement database storage for better scalability
- Enhance UI with a frontend framework

## License

This project was created by me. Feel free to contribute and enhance it!


 


