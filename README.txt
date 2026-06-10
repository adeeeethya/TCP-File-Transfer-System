# TCP File Transfer System

A Python-based client-server application that enables reliable file transfer and remote file management using TCP sockets. The server supports multiple clients simultaneously through multithreading.

## Features

-  File upload
-  File download
-  List files on the server
-  Rename files
-  Delete files
-  Create directories
-  Multithreaded server
-  Error handling and connection timeouts
-  Transfer progress display

## Technologies Used

- Python
- Socket Programming
- TCP Protocol
- Multithreading

## Project Structure

```
TCP-File-Transfer-System/
│
├── client.py
├── server.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/adeeeethya/TCP-File-Transfer-System.git
cd TCP-File-Transfer-System
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Start the server

```bash
python server.py
```

### Start the client

```bash
python client.py
```

## Requirements

- Python 3.x

## Author

**Adithya Balaji Sekhar**

GitHub: https://github.com/adeeeethya
