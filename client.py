
import socket
import os
import sys
import ctypes
from colorama import init, Fore, Back, Style

init(autoreset=True)

SERVER_IP = "127.0.0.1"
PORT = 5001
BUFFER_SIZE = 4096

def print_menu():
    """Display the main menu"""
    print(Fore.CYAN + "\n" + "="*60)
    print(Fore.YELLOW + "          TCP FILE TRANSFER CLIENT")
    print(Fore.CYAN + "="*60)
    print(Fore.GREEN + "1. List files on server")
    print("2. Download file from server")
    print("3. Upload file to server")
    print("4. Get file info (size)")
    print("5. Delete file on server")
    print("6. Rename file on server")
    print("7. Create directory on server")
    print("8. List directories on server")
    print("9. Exit")
    print(Fore.CYAN + "="*60)

def list_files():
    """Request file list from server"""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect((SERVER_IP, PORT))
        
        # Send command to list files
        client.send(b"LIST")
        
        # Receive file list
        file_list = client.recv(BUFFER_SIZE * 10).decode()
        
        if file_list:
            print("\n[SERVER FILES AVAILABLE]")
            print(file_list)
        else:
            print("No files available on server")
        
        client.close()
    except socket.timeout:
        print("ERROR: Connection timeout - Server not responding")
    except ConnectionRefusedError:
        print(f"ERROR: Cannot connect to server at {SERVER_IP}:{PORT}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

def download_file():
    """Download file from server"""
    try:
        filename = input(Fore.BLUE + "\nEnter filename to download: ").strip()
        
        if not filename:
            print(Fore.RED + "ERROR: Filename cannot be empty")
            return
        
        # Show popup notification
        ctypes.windll.user32.MessageBoxW(0, f"Starting download of file: {filename}", "Download Notification", 0)
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect((SERVER_IP, PORT))
        
        # Send DOWNLOAD command with filename
        command = f"DOWNLOAD:{filename}"
        client.send(command.encode())
        
        # Receive status
        status = client.recv(BUFFER_SIZE).decode()
        
        if status.startswith("ERROR"):
            print(f"ERROR: {status}")
            client.close()
            return
        
        if status.startswith("SIZE:"):
            file_size = int(status.split(":")[1])
            print(f"Downloading... (Size: {file_size / 1024:.2f} KB)")
        
        # Receive file
        output_filename = "downloaded_" + filename
        received_size = 0
        
        with open(output_filename, "wb") as f:
            while True:
                data = client.recv(BUFFER_SIZE)
                if not data:
                    break
                f.write(data)
                received_size += len(data)
                # Show progress
                progress = (received_size / file_size * 100) if file_size > 0 else 0
                print(f"Progress: {progress:.1f}%", end='\r')
        
        print(f"\n✓ File downloaded successfully: {output_filename}")
        client.close()
        
    except socket.timeout:
        print("ERROR: Connection timeout - Server took too long to respond")
    except ConnectionRefusedError:
        print(f"ERROR: Cannot connect to server at {SERVER_IP}:{PORT}")
    except Exception as e:
        print(f"ERROR: {str(e)}")

def upload_file():
    """Upload file to server"""
    try:
        filename = input("\nEnter path of file to upload: ").strip()
        
        if not filename or not os.path.exists(filename):
            print("ERROR: File does not exist")
            return
        
        file_size = os.path.getsize(filename)
        short_name = os.path.basename(filename)
        
        print(f"Uploading: {short_name} (Size: {file_size / 1024:.2f} KB)")
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(10)
        client.connect((SERVER_IP, PORT))
        
        # Send UPLOAD command with filename and size
        command = f"UPLOAD:{short_name}:{file_size}"
        client.send(command.encode())
        
        # Receive acknowledgment
        ack = client.recv(BUFFER_SIZE).decode()
        
        if ack != "READY":
            print(f"ERROR: Server not ready - {ack}")
            client.close()
            return
        
        # Send file
        sent_size = 0
        with open(filename, "rb") as f:
            while True:
                data = f.read(BUFFER_SIZE)
                if not data:
                    break
                client.sendall(data)
                sent_size += len(data)
                progress = (sent_size / file_size * 100)
                print(f"Progress: {progress:.1f}%", end='\r')
        
        # Receive confirmation
        response = client.recv(BUFFER_SIZE).decode()
        
        if response == "OK":
            print(f"\n✓ File uploaded successfully!")
        else:
            print(f"\nWARNING: {response}")
        
        client.close()
        
    except socket.timeout:
        print("ERROR: Connection timeout")
    except ConnectionRefusedError:
        print(f"ERROR: Cannot connect to server at {SERVER_IP}:{PORT}")
    except FileNotFoundError:
        print("ERROR: File not found")
    except Exception as e:
        print(f"ERROR: {str(e)}")

def get_file_info():
    """Get file size and info from server"""
    try:
        filename = input(Fore.BLUE + "\nEnter filename to check: ").strip()
        
        if not filename:
            print(Fore.RED + "ERROR: Filename cannot be empty")
            return
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect((SERVER_IP, PORT))
        
        # Send INFO command
        command = f"INFO:{filename}"
        client.send(command.encode())
        
        # Receive info
        info = client.recv(BUFFER_SIZE).decode()
        
        if info.startswith("ERROR"):
            print(Fore.RED + f"ERROR: {info}")
        else:
            print(Fore.GREEN + f"\n[FILE INFO]")
            print(info)
        
        client.close()
        
    except socket.timeout:
        print(Fore.RED + "ERROR: Connection timeout")
    except ConnectionRefusedError:
        print(Fore.RED + f"ERROR: Cannot connect to server at {SERVER_IP}:{PORT}")
    except Exception as e:
        print(Fore.RED + f"ERROR: {str(e)}")

def delete_file():
    """Delete file on server"""
    try:
        filename = input(Fore.BLUE + "\nEnter filename to delete: ").strip()
        
        if not filename:
            print(Fore.RED + "ERROR: Filename cannot be empty")
            return
        
        confirm = input(Fore.YELLOW + f"Are you sure you want to delete '{filename}'? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Delete cancelled.")
            return
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect((SERVER_IP, PORT))
        
        # Send DELETE command
        command = f"DELETE:{filename}"
        client.send(command.encode())
        
        # Receive response
        response = client.recv(BUFFER_SIZE).decode()
        
        if response.startswith("ERROR"):
            print(Fore.RED + f"ERROR: {response}")
        else:
            print(Fore.GREEN + response)
        
        client.close()
        
    except socket.timeout:
        print(Fore.RED + "ERROR: Connection timeout")
    except ConnectionRefusedError:
        print(Fore.RED + f"ERROR: Cannot connect to server at {SERVER_IP}:{PORT}")
    except Exception as e:
        print(Fore.RED + f"ERROR: {str(e)}")

def rename_file():
    """Rename file on server"""
    try:
        old_name = input(Fore.BLUE + "\nEnter current filename: ").strip()
        new_name = input(Fore.BLUE + "Enter new filename: ").strip()
        
        if not old_name or not new_name:
            print(Fore.RED + "ERROR: Filenames cannot be empty")
            return
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect((SERVER_IP, PORT))
        
        # Send RENAME command
        command = f"RENAME:{old_name}:{new_name}"
        client.send(command.encode())
        
        # Receive response
        response = client.recv(BUFFER_SIZE).decode()
        
        if response.startswith("ERROR"):
            print(Fore.RED + f"ERROR: {response}")
        else:
            print(Fore.GREEN + response)
        
        client.close()
        
    except socket.timeout:
        print(Fore.RED + "ERROR: Connection timeout")
    except ConnectionRefusedError:
        print(Fore.RED + f"ERROR: Cannot connect to server at {SERVER_IP}:{PORT}")
    except Exception as e:
        print(Fore.RED + f"ERROR: {str(e)}")

def create_directory():
    """Create directory on server"""
    try:
        dirname = input(Fore.BLUE + "\nEnter directory name to create: ").strip()
        
        if not dirname:
            print(Fore.RED + "ERROR: Directory name cannot be empty")
            return
        
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect((SERVER_IP, PORT))
        
        # Send MKDIR command
        command = f"MKDIR:{dirname}"
        client.send(command.encode())
        
        # Receive response
        response = client.recv(BUFFER_SIZE).decode()
        
        if response.startswith("ERROR"):
            print(Fore.RED + f"ERROR: {response}")
        else:
            print(Fore.GREEN + response)
        
        client.close()
        
    except socket.timeout:
        print(Fore.RED + "ERROR: Connection timeout")
    except ConnectionRefusedError:
        print(Fore.RED + f"ERROR: Cannot connect to server at {SERVER_IP}:{PORT}")
    except Exception as e:
        print(Fore.RED + f"ERROR: {str(e)}")

def list_directories():
    """List directories on server"""
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5)
        client.connect((SERVER_IP, PORT))
        
        # Send LISTDIR command
        client.send(b"LISTDIR")
        
        # Receive directory list
        dir_list = client.recv(BUFFER_SIZE * 10).decode()
        
        if dir_list:
            print(Fore.GREEN + "\n[SERVER DIRECTORIES]")
            print(dir_list)
        else:
            print("No directories available on server")
        
        client.close()
    except socket.timeout:
        print(Fore.RED + "ERROR: Connection timeout - Server not responding")
    except ConnectionRefusedError:
        print(Fore.RED + f"ERROR: Cannot connect to server at {SERVER_IP}:{PORT}")
def main():
    """Main client loop"""
    print(Fore.MAGENTA + "\nConnecting to server at {}:{}".format(SERVER_IP, PORT))
    
    while True:
        print_menu()
        choice = input(Fore.BLUE + "Enter your choice (1-9): ").strip()
        
        if choice == "1":
            list_files()
        elif choice == "2":
            download_file()
        elif choice == "3":
            upload_file()
        elif choice == "4":
            get_file_info()
        elif choice == "5":
            delete_file()
        elif choice == "6":
            rename_file()
        elif choice == "7":
            create_directory()
        elif choice == "8":
            list_directories()
        elif choice == "9":
            print(Fore.MAGENTA + "\nGoodbye!")
            break
        else:
            print(Fore.RED + "ERROR: Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
