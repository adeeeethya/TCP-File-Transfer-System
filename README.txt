
╔══════════════════════════════════════════════════════════════════════════════╗
║                  TCP FILE TRANSFER SYSTEM - ENHANCED VERSION                   ║
║                         Computer Networks Lab Project                          ║
╚══════════════════════════════════════════════════════════════════════════════╝

PROJECT DESCRIPTION:
═══════════════════════════════════════════════════════════════════════════════
This project implements a robust client-server file transfer system using TCP 
sockets in Python. It demonstrates practical networking concepts including socket 
programming, multi-threading, file I/O, and error handling.

KEY FEATURES:
═══════════════════════════════════════════════════════════════════════════════
✓ FILE LISTING       - View all available files on the server
✓ FILE DOWNLOAD      - Download files from server with progress tracking & popup notification
✓ FILE UPLOAD        - Upload files to server with size validation
✓ FILE INFO          - Get file details (size, modification time)
✓ FILE DELETE        - Delete files on server with confirmation
✓ FILE RENAME        - Rename files on server
✓ DIRECTORY CREATE   - Create directories on server
✓ DIRECTORY LISTING  - View all directories on server
✓ MULTI-THREADING    - Server handles multiple clients simultaneously
✓ ERROR HANDLING     - Comprehensive error checking and reporting
✓ PROGRESS TRACKING  - Real-time progress display during transfers
✓ LOGGING            - Timestamped server logs for monitoring
✓ CONNECTION TIMEOUT - Prevents hanging connections
✓ INPUT VALIDATION   - Prevents directory traversal attacks
✓ COLORED INTERFACE  - Enhanced visual appearance with colors

NETWORKING CONCEPTS DEMONSTRATED:
═══════════════════════════════════════════════════════════════════════════════
1. TCP Socket Programming (AF_INET, SOCK_STREAM)
2. Server-Client Architecture
3. Connection Handling and Management
4. Binary Data Transmission
5. Error Recovery and Validation
6. Threading for Concurrent Client Handling
7. Buffered I/O Operations
8. Protocol Design (Custom command format)
9. Connection Timeout Handling
10. Resource Cleanup

REQUIREMENTS:
═══════════════════════════════════════════════════════════════════════════════
- Python 3.6 or higher installed
- Windows/Linux/Mac with socket support
- Network connectivity (localhost in this setup)
- colorama library (pip install colorama)

HOW TO RUN:
═══════════════════════════════════════════════════════════════════════════════

OPTION 1: Using Batch Files (Windows Only)
─────────────────────────────────────────
1. Click "run_server.bat"     -> Starts the server (runs server.py)
2. Click "run_client.bat"     -> Starts the client (runs client.py)
3. Follow the menu options in the client

OPTION 2: Using Command Prompt / PowerShell (Standard Method)
─────────────────────────────────────────────────────────────

Step 1: Start the Server
   A. Open Command Prompt / PowerShell in the project folder
   B. Run: python server.py
   C. You should see:
      
      [timestamp] ============================================================
      [timestamp] TCP FILE TRANSFER SERVER STARTED
      [timestamp] ============================================================
      [timestamp] Listening on 0.0.0.0:5001
      [timestamp] Server directory: C:\path\to\project
      [timestamp] Available files: 2
      [timestamp] ============================================================
      [timestamp] Waiting for client connections...

   D. Leave this terminal running

Step 2: Start the Client (in ANOTHER terminal/window)
   A. Open a NEW Command Prompt / PowerShell
   B. Navigate to the same project folder
   C. Run: python client.py
   D. A menu will appear with options:
      
      ============================================================
             TCP FILE TRANSFER CLIENT
      ============================================================
      1. List files on server
      2. Download file from server
      3. Upload file to server
      4. Get file info (size)
      5. Delete file on server
      6. Rename file on server
      7. Create directory on server
      8. List directories on server
      9. Exit
      ============================================================

STEP-BY-STEP USAGE EXAMPLES:
═══════════════════════════════════════════════════════════════════════════════

EXAMPLE 1: List Files on Server
──────────────────────────────
   Client Menu: Choose option "1"
   
   Output:
   ✓ Connects to server
   ✓ Opens terminal showing available files with sizes
   
   Server Log:
   [timestamp] New connection from ('127.0.0.1', 12345)
   [timestamp] Sent file list to ('127.0.0.1', 12345)
   [timestamp] Connection closed: ('127.0.0.1', 12345)

EXAMPLE 2: Download File from Server
─────────────────────────────────────
   Client Menu: Choose option "2"
   Input: test.txt
   
   Output:
   Downloading... (Size: 50.25 KB)
   Progress: 100.0%
   ✓ File downloaded successfully: downloaded_test.txt
   
   Server Log:
   [timestamp] New connection from ('127.0.0.1', 12346)
   [timestamp] ✓ Downloaded 'test.txt' (50.25 KB) by ('127.0.0.1', 12346)
   [timestamp] Connection closed: ('127.0.0.1', 12346)

EXAMPLE 3: Upload File to Server
────────────────────────────────
   Client Menu: Choose option "3"
   Input: C:\path\to\myfile.pdf
   
   Output:
   Uploading: myfile.pdf (Size: 102.50 KB)
   Progress: 100.0%
   ✓ File uploaded successfully!
   
   Server Log:
   [timestamp] New connection from ('127.0.0.1', 12347)
   [timestamp] Receiving upload: 'myfile.pdf' (102.50 KB) from ('127.0.0.1', 12347)
   [timestamp] ✓ Uploaded 'myfile.pdf' successfully (from ('127.0.0.1', 12347))

EXAMPLE 4: Get File Information
───────────────────────────────
   Client Menu: Choose option "4"
   Input: test.txt
   
   Output:
   [FILE INFO]
   Filename: test.txt
   Size: 51456 bytes (50.25 KB)
   Modified: Wed Mar 13 14:32:10 2024

WHAT EACH FILE DOES:
═══════════════════════════════════════════════════════════════════════════════

server.py
─────────
• Listens on port 5001 for incoming client connections
• Handles multiple clients simultaneously using threads
• Supports commands: LIST, DOWNLOAD, UPLOAD, INFO
• Provides file size and modification information
• Logs all activities with timestamps
• Validates filenames to prevent directory traversal attacks
• Graceful error handling and connection cleanup

Key Functions:
  - start_server()       : Main server loop, accepts connections
  - handle_client()      : Processes individual client requests (threaded)
  - handle_list_request(): Returns list of available files
  - handle_download_request(): Sends file to client
  - handle_upload_request(): Receives file from client
  - handle_info_request(): Provides file details
  - log_message()        : Log events with timestamps

client.py
─────────
• Connects to server at 127.0.0.1:5001
• User-friendly menu-driven interface
• Supports all server commands with proper error handling
• Shows progress during file transfers
• Validates user input before sending requests
• Automatic retry and timeout handling

Key Functions:
  - main()           : Main client loop with menu
  - list_files()     : Request and display available files
  - download_file()  : Download file with progress tracking
  - upload_file()    : Upload file with validation
  - get_file_info()  : Get file details from server
  - print_menu()     : Display menu options

COMMON ERRORS & SOLUTIONS:
═══════════════════════════════════════════════════════════════════════════════

ERROR: "Cannot connect to server at 127.0.0.1:5001"
─────────────────────────────────────────────────
Cause: Server is not running or port is unavailable
Solution: 
  1. Make sure server.py is running in another terminal
  2. Check if port 5001 is already in use
  3. Restart both server and client

ERROR: "File not found on server"
────────────────────────────────
Cause: Requested file doesn't exist in server directory
Solution:
  1. Use option "1" to list available files
  2. Make sure file is in the same folder as server.py
  3. Check spelling of filename

ERROR: "Connection timeout - Server took too long"
──────────────────────────────────────────────
Cause: Server crashed or network issue
Solution:
  1. Check server terminal for error messages
  2. Restart server.py
  3. Try again with a smaller file

ERROR: "Port 5001 may already be in use"
──────────────────────────────────────
Cause: Another application is using port 5001
Solution:
  1. Restart your computer
  2. Find and close application using port 5001
  3. Edit PORT = 5001 in both files to use different port (e.g., 5002)

TESTING SCENARIOS:
═══════════════════════════════════════════════════════════════════════════════

Test 1: Basic Download
───────────────────
1. Start server
2. Start client
3. Press "1" to see available files
4. Press "2" to download "test.txt"
5. Check that "downloaded_test.txt" appears
Expected: File should be downloaded with progress shown

Test 2: File Upload
──────────────────
1. Server is running
2. Client running
3. Create a test file on your computer
4. Press "3" in client menu
5. Enter path to test file
Expected: File appears in server directory

Test 3: Multiple Clients
───────────────────────
1. Start one server
2. Start multiple clients in different terminals
3. Have them download/upload simultaneously
Expected: Server should handle all requests without corruption

Test 4: Large File Transfer
───────────────────────────
1. Create a large file (>10MB)
2. Try uploading via client
3. Observe progress tracking
Expected: Transfer should complete with accurate progress display

PERFORMANCE NOTES:
═══════════════════════════════════════════════════════════════════════════════
• BUFFER_SIZE = 4096 bytes provides good balance between speed and memory
• Larger files may take time due to Python's I/O performance
• Threading allows server to handle multiple clients
• Socket timeout set to 30 seconds to prevent hanging

SECURITY CONSIDERATIONS:
═══════════════════════════════════════════════════════════════════════════════
⚠ This is for educational purposes only
⚠ Currently runs on localhost without encryption
⚠ No authentication mechanism implemented
⚠ For production use, add:
  - SSL/TLS encryption
  - User authentication
  - File access permissions
  - Input validation and sanitization

IMPROVEMENTS MADE FROM BASIC VERSION:
═══════════════════════════════════════════════════════════════════════════════
1. ✓ Multi-threading support for multiple clients
2. ✓ File listing capability
3. ✓ Upload functionality (bidirectional transfer)
4. ✓ File information/details display
5. ✓ Progress tracking during transfers
6. ✓ Comprehensive error handling with try-catch
7. ✓ User-friendly menu interface
8. ✓ Timestamped logging system
9. ✓ Connection timeout handling
10. ✓ Input validation and security checks
11. ✓ Better formatted output and messages
12. ✓ Proper resource cleanup on disconnection

═══════════════════════════════════════════════════════════════════════════════
Author: Computer Networks Lab
Date: March 2024
IDE Tested: VS Code, PyCharm
Python Version: 3.6+
═══════════════════════════════════════════════════════════════════════════════
