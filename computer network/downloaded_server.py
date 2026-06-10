
import socket
import os
import threading
import time
from datetime import datetime

HOST = '0.0.0.0'
PORT = 5001
BUFFER_SIZE = 4096

# Lock for thread-safe file operations
file_lock = threading.Lock()

def log_message(message):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def get_file_list():
    """Get list of files available on server"""
    try:
        files = []
        for file in os.listdir("."):
            if os.path.isfile(file):
                size = os.path.getsize(file)
                files.append(f"  • {file:<30} ({size / 1024:.2f} KB)")
        
        if not files:
            return "No files available"
        
        return "Available files:\n" + "\n".join(files)
    except Exception as e:
        return f"ERROR: {str(e)}"

def handle_list_request(conn):
    """Handle LIST command from client"""
    try:
        file_list = get_file_list()
        conn.send(file_list.encode())
        log_message(f"Sent file list to {conn.getpeername()}")
    except Exception as e:
        log_message(f"ERROR sending file list: {str(e)}")

def handle_download_request(conn, filename):
    """Handle DOWNLOAD command from client"""
    try:
        if not os.path.exists(filename):
            conn.send(b"ERROR: File not found")
            log_message(f"Download failed - file '{filename}' not found (from {conn.getpeername()})")
            return
        
        # Check if it's a file (not directory)
        if not os.path.isfile(filename):
            conn.send(b"ERROR: Not a file")
            log_message(f"Download failed - '{filename}' is not a file (from {conn.getpeername()})")
            return
        
        file_size = os.path.getsize(filename)
        
        # Send size information
        conn.send(f"SIZE:{file_size}".encode())
        time.sleep(0.1)  # Small delay to ensure client receives size first
        
        # Send file
        with open(filename, "rb") as f:
            sent_bytes = 0
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                conn.sendall(data)
                sent_bytes += len(data)
        
        log_message(f"✓ Downloaded '{filename}' ({file_size / 1024:.2f} KB) by {conn.getpeername()}")
        
    except Exception as e:
        log_message(f"ERROR during download: {str(e)}")
        try:
            conn.send(f"ERROR: {str(e)}".encode())
        except:
            pass

def handle_upload_request(conn, data):
    """Handle UPLOAD command from client"""
    try:
        parts = data.split(":")
        if len(parts) < 3:
            conn.send(b"ERROR: Invalid upload format")
            return
        
        filename = parts[1]
        try:
            file_size = int(parts[2])
        except ValueError:
            conn.send(b"ERROR: Invalid file size")
            return
        
        # Validate filename
        if "/" in filename or "\\" in filename:
            conn.send(b"ERROR: Invalid filename")
            return
        
        # Send ready signal
        conn.send(b"READY")
        
        log_message(f"Receiving upload: '{filename}' ({file_size / 1024:.2f} KB) from {conn.getpeername()}")
        
        # Receive file
        with file_lock:
            with open(filename, "wb") as f:
                received_bytes = 0
                while received_bytes < file_size:
                    to_receive = min(BUFFER_SIZE, file_size - received_bytes)
                    data = conn.recv(to_receive)
                    if not data:
                        break
                    f.write(data)
                    received_bytes += len(data)
        
        # Sendconfirmation
        if received_bytes == file_size:
            conn.send(b"OK")
            log_message(f"✓ Uploaded '{filename}' successfully (from {conn.getpeername()})")
        else:
            conn.send(b"ERROR: Incomplete upload")
            log_message(f"WARNING: Incomplete upload of '{filename}'")
        
    except Exception as e:
        log_message(f"ERROR during upload: {str(e)}")
        try:
            conn.send(f"ERROR: {str(e)}".encode())
        except:
            pass

def handle_info_request(conn, filename):
    """Handle INFO command from client"""
    try:
        if not os.path.exists(filename):
            conn.send(b"ERROR: File not found")
            return
        
        if not os.path.isfile(filename):
            conn.send(b"ERROR: Not a file")
            return
        
        file_size = os.path.getsize(filename)
        mod_time = time.ctime(os.path.getmtime(filename))
        
        info = f"Filename: {filename}\nSize: {file_size} bytes ({file_size / 1024:.2f} KB)\nModified: {mod_time}"
        conn.send(info.encode())
        log_message(f"Sent file info for '{filename}' to {conn.getpeername()}")
        
    except Exception as e:
        log_message(f"ERROR getting file info: {str(e)}")
        try:
            conn.send(f"ERROR: {str(e)}".encode())
        except:
            pass

def handle_delete_request(conn, filename):
    """Handle DELETE command from client"""
    try:
        if not os.path.exists(filename):
            conn.send(b"ERROR: File not found")
            log_message(f"Delete failed - file '{filename}' not found (from {conn.getpeername()})")
            return
        
        if not os.path.isfile(filename):
            conn.send(b"ERROR: Not a file")
            log_message(f"Delete failed - '{filename}' is not a file (from {conn.getpeername()})")
            return
        
        os.remove(filename)
        conn.send(b"File deleted successfully")
        log_message(f"✓ Deleted '{filename}' (from {conn.getpeername()})")
        
    except Exception as e:
        log_message(f"ERROR during delete: {str(e)}")
        try:
            conn.send(f"ERROR: {str(e)}".encode())
        except:
            pass

def handle_rename_request(conn, data):
    """Handle RENAME command from client"""
    try:
        parts = data.split(":")
        if len(parts) < 3:
            conn.send(b"ERROR: Invalid rename format")
            return
        
        old_name = parts[1]
        new_name = parts[2]
        
        if not os.path.exists(old_name):
            conn.send(b"ERROR: File not found")
            log_message(f"Rename failed - file '{old_name}' not found (from {conn.getpeername()})")
            return
        
        if "/" in new_name or "\\" in new_name:
            conn.send(b"ERROR: Invalid new filename")
            return
        
        os.rename(old_name, new_name)
        conn.send(b"File renamed successfully")
        log_message(f"✓ Renamed '{old_name}' to '{new_name}' (from {conn.getpeername()})")
        
    except Exception as e:
        log_message(f"ERROR during rename: {str(e)}")
        try:
            conn.send(f"ERROR: {str(e)}".encode())
        except:
            pass

def handle_mkdir_request(conn, dirname):
    """Handle MKDIR command from client"""
    try:
        if "/" in dirname or "\\" in dirname:
            conn.send(b"ERROR: Invalid directory name")
            return
        
        if os.path.exists(dirname):
            conn.send(b"ERROR: Directory already exists")
            return
        
        os.makedirs(dirname)
        conn.send(b"Directory created successfully")
        log_message(f"✓ Created directory '{dirname}' (from {conn.getpeername()})")
        
    except Exception as e:
        log_message(f"ERROR during mkdir: {str(e)}")
        try:
            conn.send(f"ERROR: {str(e)}".encode())
        except:
            pass

def handle_listdir_request(conn):
    """Handle LISTDIR command from client"""
    try:
        dirs = []
        for item in os.listdir("."):
            if os.path.isdir(item):
                dirs.append(f"  • {item}")
        
        if not dirs:
            conn.send(b"No directories available")
        else:
            result = "Available directories:\n" + "\n".join(dirs)
            conn.send(result.encode())
        
        log_message(f"Sent directory list to {conn.getpeername()}")
    except Exception as e:
        log_message(f"ERROR sending directory list: {str(e)}")
        try:
            conn.send(b"ERROR: Failed to list directories")
        except:
            pass

def handle_client(conn, addr):
    """Handle individual client connection"""
    try:
        log_message(f"New connection from {addr}")
        conn.settimeout(30)
        
        # Receive command
        data = conn.recv(BUFFER_SIZE).decode()
        
        if data.startswith("LIST"):
            handle_list_request(conn)
        elif data.startswith("DOWNLOAD:"):
            filename = data[9:]  # Remove "DOWNLOAD:" prefix
            handle_download_request(conn, filename)
        elif data.startswith("UPLOAD:"):
            handle_upload_request(conn, data)
        elif data.startswith("INFO:"):
            filename = data[5:]  # Remove "INFO:" prefix
            handle_info_request(conn, filename)
        elif data.startswith("DELETE:"):
            filename = data[7:]  # Remove "DELETE:" prefix
            handle_delete_request(conn, filename)
        elif data.startswith("RENAME:"):
            handle_rename_request(conn, data)
        elif data.startswith("MKDIR:"):
            dirname = data[6:]  # Remove "MKDIR:" prefix
            handle_mkdir_request(conn, dirname)
        elif data.startswith("LISTDIR"):
            handle_listdir_request(conn)
        else:
            log_message(f"Unknown command from {addr}: {data[:50]}")
            conn.send(b"ERROR: Unknown command")
        
    except socket.timeout:
        log_message(f"Timeout - {addr} did not send data")
    except Exception as e:
        log_message(f"ERROR handling client {addr}: {str(e)}")
    finally:
        try:
            conn.close()
        except:
            pass
        log_message(f"Connection closed: {addr}")

def start_server():
    """Start the TCP server"""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)
        
        log_message("="*60)
        log_message("TCP FILE TRANSFER SERVER STARTED")
        log_message("="*60)
        log_message(f"Listening on {HOST}:{PORT}")
        log_message(f"Server directory: {os.getcwd()}")
        log_message(f"Available files: {len([f for f in os.listdir('.') if os.path.isfile(f)])}")
        log_message("="*60)
        log_message("Waiting for client connections...")
        
        while True:
            try:
                conn, addr = server.accept()
                # Create thread to handle client
                client_thread = threading.Thread(target=handle_client, args=(conn, addr))
                client_thread.daemon = True
                client_thread.start()
            except KeyboardInterrupt:
                log_message("\nServer shutdown requested")
                break
            except Exception as e:
                log_message(f"ERROR accepting connection: {str(e)}")
    
    except socket.error as e:
        log_message(f"FATAL ERROR: Cannot start server - {str(e)}")
        log_message(f"Port {PORT} may already be in use. Try closing other applications or use a different port.")
    except KeyboardInterrupt:
        log_message("\nServer interrupted")
    except Exception as e:
        log_message(f"FATAL ERROR: {str(e)}")
    finally:
        try:
            server.close()
        except:
            pass
        log_message("Server stopped")

if __name__ == "__main__":
    start_server()
