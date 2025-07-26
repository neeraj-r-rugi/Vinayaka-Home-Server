# Vinayaka Home Server

A simple Flask-based web server that provides secure access to files and directories on your local machine from any device connected to your home network. Perfect for students who want to access their files remotely within their local network.

## ⚠️ Important Security Disclaimer

**READ THIS CAREFULLY BEFORE USING THIS SERVER**

This server is designed **ONLY** for use on safe, secured, and trusted networks such as:
- Your personal home WiFi network
- Your personal mobile hotspot
- Other networks you completely trust and control

**NEVER use this server on:**
- Public WiFi networks (coffee shops, airports, hotels, etc.)
- University or workplace networks
- Any network you don't personally control
- Networks with unknown or untrusted users

**Additional Safety Requirements:**
- **NEVER leave the server running unattended** - Always stop the server when you're not actively using it
- **NEVER expose this server to the internet** - This is for local network use only
- **NEVER use weak passwords** - Use a strong, unique password
- **NEVER run this on a network with people you don't trust** - Anyone on the network can potentially access your files if they discover the server

**Why these restrictions matter:**
- This server provides direct access to your file system
- It uses basic authentication that may be vulnerable on untrusted networks
- Malicious users on the same network could potentially discover and exploit the server
- Running unattended increases the risk of unauthorized access

**Your responsibility:** You are solely responsible for ensuring this server is used safely and securely. The authors are not responsible for any data loss, security breaches, or other issues that may arise from improper use.

By using this server, you acknowledge that you understand these risks and will only use it in appropriate, secure environments.

## Features

- **Password Protection**: Secure login system to prevent unauthorized access
- **Directory Navigation**: Browse through folders and files with an intuitive web interface
- **File Serving**: Direct file access and download capabilities
- **ZIP Downloads**: Download entire folders as ZIP archives
- **Network Access**: Access your files from any device on your local network
- **Security Controls**: Path traversal protection and directory exclusion
- **Command-Line Configuration**: Easy setup with command-line arguments
- **Debug Mode**: Optional debug mode for development
- **Clean UI**: Modern, responsive design with JetBrains Mono font

## Prerequisites

- Python 3.6 or higher
- Flask web framework
- A local network (WiFi/Ethernet)

## Installation

1. **Clone or download the project files**
   ```bash
   git clone <repository-url>
   cd vinayaka-home-server
   ```

2. **Install Flask**
   ```bash
   pip install flask
   ```

3. **Create the required directory structure**
   ```
   project-folder/
   ├── server.py
   ├── util.py
   ├── templates/
   │   ├── index.html
   │   └── dashboard.html
   └── static/
       ├── index_style.css
       └── dash_style.css
   ```

## Quick Start

### Basic Usage
The simplest way to start the server with default settings:

```bash
python server.py
```

This will:
- Use `/media/neeraj-r-rugi/NEERAJ_DRIVE` as the default directory
- Set password to "Dingus" (change this for security!)
- Start the server on `http://0.0.0.0:5000`

### Command-Line Options

The server supports several command-line arguments for easy configuration:

```bash
python server.py [OPTIONS]
```

#### Available Options:

| Option | Short | Description | Default |
|--------|--------|-------------|---------|
| `--data-dir` | `-dr` | Directory to serve files from | `/media/neeraj-r-rugi/NEERAJ_DRIVE` |
| `--password` | `-ps` | Password for server access | `Dingus` |
| `--exclude-dir` | `-ed` | Directories to exclude (space-separated) | None |
| `--debug` | `-db` | Enable Flask debug mode | Disabled |
| `--help` | `-h` | Show help message | - |

#### Usage Examples:

**Basic configuration with custom directory and password:**
```bash
python server.py --data-dir "/home/username/Documents" --password "MySecurePassword123"
```

**Exclude specific directories:**
```bash
python server.py --data-dir "/home/user/files" --exclude-dir "Private" "Confidential" "Personal"
```

**Enable debug mode for development:**
```bash
python server.py --debug --password "DevPassword"
```

**Full configuration example:**
```bash
python server.py \
    --data-dir "/Users/john/SharedFiles" \
    --password "SuperSecurePassword2024" \
    --exclude-dir "Private" "Work" "Confidential" \
    --debug
```

**Windows example:**
```cmd
python server.py --data-dir "C:\Users\YourName\Documents" --password "YourPassword"
```

## Configuration

### Method 1: Command-Line Arguments (Recommended)
Use the command-line options as shown above for quick and easy configuration.

### Method 2: Code Modification (Legacy)
You can also modify the default values directly in `util.py`:

```python
def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="VinayakaHomeServer", description="A Local WAN Home Data Server")
    parser.add_argument("--data-dir", "-dr",
                        default="/your/custom/directory",  # Change this
                        help="The Directory which the server is to host.")
    parser.add_argument("--password", "-ps",
                        default="YourSecurePassword",      # Change this
                        help="The Password for Logging into your server.")
    # ... rest of the configuration
```

## Usage

### Starting the Server

1. **Navigate to the project directory**
   ```bash
   cd /path/to/vinayaka-home-server
   ```

2. **Run the server with your desired configuration**
   ```bash
   # Example: Custom directory and password
   python server.py --data-dir "/home/user/files" --password "MyPassword123"
   ```

3. **Server will start and display connection information**
   ```
   * Running on all addresses (0.0.0.0)
   * Running on http://127.0.0.1:5000
   * Running on http://[your-local-ip]:5000
   ```

### Accessing from Other Devices

1. **Find your computer's local IP address**
   - **Windows**: Open Command Prompt and run `ipconfig`
   - **macOS/Linux**: Open Terminal and run `ifconfig` or `ip addr show`

2. **Connect from any device on your network**
   - Open a web browser on any device connected to the same network
   - Navigate to: `http://[your-computer-ip]:5000`
   - Example: `http://192.168.1.100:5000`

3. **Login with your configured password**
   - Enter the password you set with `--password` or the default "Dingus"
   - Click "Login" to access the file browser

### Navigation Features

- **Browse Directories**: Click on folder names (marked with `/`) to navigate into them
- **Download Files**: Click on file names to view or download them
- **Download Folders**: Use "📦 Download Folder as ZIP" to download entire directories
- **Go Back**: Use "🔼 Up One Directory" to go back to the parent directory
- **Return Home**: Click "⬅️ Return Home" to go back to the base directory
- **Breadcrumb Navigation**: Use the path navigation at the top to jump to any parent directory

## Security Features

### Built-in Security
- **Password Authentication**: Session-based login system with configurable passwords
- **Path Traversal Protection**: Prevents access to directories outside the base directory
- **Directory Exclusion**: Hide sensitive directories from the web interface using `--exclude-dir`
- **Session Management**: Secure session handling with randomly generated secret keys
- **Input Validation**: Proper validation of file paths and user inputs

### Security Best Practices
1. **Use a Strong Password**: Always change from the default "Dingus" password
   ```bash
   python server.py --password "YourStrongPassword123!"
   ```

2. **Exclude Sensitive Directories**: Hide private folders from the web interface
   ```bash
   python server.py --exclude-dir "Private" "Personal" "Confidential"
   ```

3. **Local Network Only**: This server is designed for local network use only
4. **Firewall Configuration**: Ensure your firewall is properly configured
5. **Regular Updates**: Keep Python and Flask updated to the latest versions

## Advanced Configuration

### Environment-Specific Examples

**Student Setup:**
```bash
python server.py \
    --data-dir "/home/student/Documents" \
    --password "StudyFiles2024" \
    --exclude-dir "Private" "Personal"
```

**Developer Setup:**
```bash
python server.py \
    --data-dir "/home/dev/Projects" \
    --password "DevAccess123" \
    --exclude-dir ".git" "node_modules" "venv" \
    --debug
```

**Media Server Setup:**
```bash
python server.py \
    --data-dir "/media/external/Movies" \
    --password "MediaAccess2024" \
    --exclude-dir "Private" "Personal"
```

### Multiple Configurations
You can create shell scripts or batch files for different configurations:

**Linux/macOS (server-config.sh):**
```bash
#!/bin/bash
python server.py \
    --data-dir "/home/user/SharedFiles" \
    --password "MySecurePassword" \
    --exclude-dir "Private" "Work"
```

**Windows (server-config.bat):**
```batch
@echo off
python server.py ^
    --data-dir "C:\Users\%USERNAME%\Documents" ^
    --password "MySecurePassword" ^
    --exclude-dir "Private" "Work"
```

## Troubleshooting

### Common Issues

1. **Cannot connect from other devices**
   - Verify both devices are on the same network
   - Check firewall settings on the host computer
   - Ensure the server is running and listening on `0.0.0.0`

2. **Permission denied errors**
   - Ensure the user running the server has read permissions for the specified `--data-dir`
   - Check directory permissions: `ls -la /path/to/directory`

3. **Files not displaying**
   - Verify the `--data-dir` path is correct and exists
   - Check if directories are listed in `--exclude-dir`

4. **Login issues**
   - Verify the password matches exactly (case-sensitive)
   - Clear browser cookies and try again

5. **Command-line argument errors**
   - Use `python server.py --help` to see all available options
   - Ensure paths with spaces are properly quoted
   - On Windows, use forward slashes or escaped backslashes in paths

### Getting Help
```bash
# Display all available options and their descriptions
python server.py --help
```

### Network Troubleshooting
```bash
# Test if server is accessible locally
curl http://localhost:5000

# Find your IP address
# Linux/macOS:
ip addr show | grep inet
# Windows:
ipconfig
```

## Development

### Project Structure
```
vinayaka-home-server/
├── server.py              # Main Flask application
├── util.py                # Command-line argument parser
├── templates/
│   ├── index.html          # Login page template
│   └── dashboard.html      # File browser template
└── static/
    ├── index_style.css     # Login page styles
    └── dash_style.css      # Dashboard styles
```

### Key Components
- **Flask Routes**: Handle authentication and file serving
- **Argument Parser**: Command-line configuration management
- **Template Engine**: Jinja2 templates for dynamic HTML generation
- **Session Management**: Secure login state management
- **File System Integration**: Safe directory traversal and file serving
- **ZIP Generation**: In-memory ZIP creation for folder downloads

### Adding Custom Features
The modular design makes it easy to extend functionality:
- **File upload**: Add upload routes and forms
- **User management**: Implement multiple user accounts
- **File search**: Add search functionality across directories
- **Thumbnails**: Generate previews for images and documents

## License

This project is provided under the GNU GPL V3.0 License.

## Contributing

This is a student project, but suggestions and improvements are welcome! Feel free to:
- Report bugs or security issues
- Suggest new features or command-line options
- Submit pull requests with improvements
- Improve documentation and examples

---

**Remember: Always prioritize security when using this server. Only use it on trusted networks and with strong passwords!**