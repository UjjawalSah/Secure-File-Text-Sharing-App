# File and Text Sharing Web App

## Overview

This web application is designed to facilitate the sharing of files and text snippets through a simple, user-friendly interface. Users can upload files or input text, which the application then assigns a unique code. This code can be shared with others, who can then use it to download the file or view the text. The application is built using Java Servlets and runs on an Apache Tomcat server. 

## Key Features

1. **File Upload and Code Generation**: Users can upload files or input text through a web form. Once the file or text is submitted, the application generates a unique code associated with the uploaded content.

2. **Code-Based Retrieval**: Users can retrieve the uploaded file or text by entering the unique code into a form on the website. The application verifies the code and, if valid, allows the user to download the file or view the text.

## How It Works

### Upload Process

1. **File/Text Submission**: The user submits a file or text through an HTML form on the web application.
2. **Code Generation**: The application generates a unique identifier (UUID) for the uploaded content.
3. **Storage**: The file or text, along with its unique code, is stored on the server in a designated directory.
4. **Code Display**: The application displays the unique code to the user, which can be shared with others to access the content.

### Retrieval Process

1. **Code Entry**: The user enters the unique code into a form on the web application.
2. **Validation**: The application checks the entered code against the stored files/texts.
3. **File/Text Retrieval**: If the code is valid, the application retrieves the corresponding file or text and allows the user to download or view it.

## Technologies Used

- **Java Servlets**: For handling HTTP requests and responses.
- **Apache Tomcat**: As the web server and servlet container.
- **HTML/CSS**: For the web interface.
- **UUID**: For generating unique codes.

## Benefits

- **Ease of Sharing**: Users can easily share files and text by simply providing a code.
- **Security**: Only users with the correct code can access the shared content.
- **Simplicity**: The application is straightforward and easy to use, with no need for complex configurations or databases.

## Use Cases

- **Collaborative Projects**: Team members can share files and text snippets quickly and easily.
- **Educational Purposes**: Teachers can share assignments and notes with students using unique codes.
- **Temporary File Storage**: Users can temporarily store files and share access with others without needing cloud storage accounts.

## Conclusion

This File and Text Sharing Web App provides a simple yet effective solution for sharing files and text snippets using unique codes. Its straightforward design and implementation make it accessible and useful for a variety of users and use cases.

https://github.com/UjjawalSah/NimbusFiles/assets/116669610/541435cb-fd8a-4f57-9c0e-3f6f77e80211

