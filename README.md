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
- **Network Access**: Access your files from any device on your local network
- **Security Controls**: Path traversal protection and directory exclusion
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
   ├── templates/
   │   ├── index.html
   │   └── dashboard.html
   └── static/
       ├── index_style.css
       └── dash_style.css
   ```

## Configuration

### 1. Set Your Base Directory
Edit `server.py` and modify the `BASE_DIR` variable to point to the directory you want to share:

```python
BASE_DIR = "/path/to/your/directory"  # Change this to your desired directory
```

**Example configurations:**
- Linux/macOS: `BASE_DIR = "/home/username/Documents"`
- Windows: `BASE_DIR = "C:\\Users\\username\\Documents"`

### 2. Change the Default Password
For security, change the default password in `server.py`:

```python
PASSWORD = "YourSecurePassword"  # Change from "Dingus" to something secure
```

### 3. Configure Directory Exclusions (Optional)
Add directories you want to hide from the web interface:

```python
EXCLUDED_DIRS = ["Private", "Confidential", "Neeraj"]  # Add directories to exclude
```

## Usage

### Starting the Server

1. **Navigate to the project directory**
   ```bash
   cd /path/to/vinayaka-home-server
   ```

2. **Run the server**
   ```bash
   python server.py
   ```

3. **Server will start on port 5000**
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

3. **Login with your password**
   - Enter the password you configured in `server.py`
   - Click "Login" to access the file browser

### Navigation

- **Browse Directories**: Click on folder names (marked with `/`) to navigate into them
- **Download Files**: Click on file names to view or download them
- **Go Back**: Use ".. (Up one)" to go back to the parent directory
- **Return Home**: Click "--RETURN HOME--" to go back to the base directory

## Security Features

### Built-in Security
- **Password Authentication**: Session-based login system
- **Path Traversal Protection**: Prevents access to directories outside the base directory
- **Directory Exclusion**: Hide sensitive directories from the web interface
- **Session Management**: Secure session handling with randomly generated secret keys

### Security Best Practices
1. **Use a Strong Password**: Choose a complex password that's difficult to guess
2. **Local Network Only**: This server is designed for local network use only
3. **Firewall Configuration**: Ensure your firewall is properly configured
4. **Regular Updates**: Keep Python and Flask updated to the latest versions

## Customization

### Styling
- Modify `static/index_style.css` to customize the login page appearance
- Modify `static/dash_style.css` to customize the file browser interface

### Server Configuration
- **Change Port**: Modify the port in `server.run(host="0.0.0.0", port=5000)`
- **Host Binding**: Change `host` parameter to limit network access

### Adding Features
The Flask application is modular and can be extended with additional features such as:
- File upload functionality
- User management
- File search capabilities
- Download statistics

## Troubleshooting

### Common Issues

1. **Cannot connect from other devices**
   - Verify both devices are on the same network
   - Check firewall settings on the host computer
   - Ensure the server is running and listening on `0.0.0.0`

2. **Permission denied errors**
   - Ensure the user running the server has read permissions for the base directory
   - Check directory permissions: `ls -la /path/to/directory`

3. **Files not displaying**
   - Verify the `BASE_DIR` path is correct and exists
   - Check if directories are listed in `EXCLUDED_DIRS`

4. **Login issues**
   - Verify the password matches exactly (case-sensitive)
   - Clear browser cookies and try again

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
├── templates/
│   ├── index.html          # Login page template
│   └── dashboard.html      # File browser template
└── static/
    ├── index_style.css     # Login page styles
    └── dash_style.css      # Dashboard styles
```

### Key Components
- **Flask Routes**: Handle authentication and file serving
- **Template Engine**: Jinja2 templates for dynamic HTML generation
- **Session Management**: Secure login state management
- **File System Integration**: Safe directory traversal and file serving

## License

This project is created for educational purposes. It is provided under the GNU GPL V3.0 License

## Contributing

This is a student project, but suggestions and improvements are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

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