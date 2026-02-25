# XPanel Security Testing Tool 🔒

## ⚠️ LEGAL DISCLAIMER & WARNING

**THIS TOOL IS FOR AUTHORIZED SECURITY TESTING ONLY!**

By using this software, you agree to the following terms:
- ✅ **ONLY** use on systems you own or have explicit written permission to test
- ✅ **ONLY** for legitimate security assessments and penetration testing
- ❌ **NEVER** use against systems without proper authorization
- ❌ **NEVER** use for illegal activities or unauthorized access

**UNAUTHORIZED ACCESS TO COMPUTER SYSTEMS IS A CRIMINAL OFFENSE!**
The developers assume NO liability and are NOT responsible for any misuse or damage caused by this program. Users are solely responsible for complying with all applicable local, state, national, and international laws.

## 📋 Overview

A multi-threaded security testing tool designed to identify XPanel instances with default credentials. This tool helps security professionals and system administrators identify vulnerable XPanel installations that still use factory default credentials.

## 🔧 Features

- **Multi-threaded Architecture**: Fast scanning with configurable thread count
- **Smart Detection**: Identifies XPanel instances by analyzing page titles
- **Colored Output**: Easy-to-read console output with color coding
- **Result Logging**: Automatically saves findings to organized files
- **Password Protection**: Built-in authentication for tool access
- **Timeout Control**: Configurable request timeout settings

## 📦 Requirements

pip install -r requirements.txt

### Dependencies
- requests
- beautifulsoup4
- colorama
- art
- pwinput
- loguru
- argparse

## 🚀 Installation
```bash
git clone https://github.com/yourusername/xpanel-security-tester.git
cd xpanel-security-tester
pip install -r requirements.txt
```
## 💻 Usage

### Basic Syntax
```bash
python xpanel_tester.py -h <hostname_file> -t <threads> --timeout <seconds>
```
### Command Line Arguments

| Argument | Description | Default | Required |
|----------|-------------|---------|----------|
| `-h, --hostname` | Path to file containing target hostnames | - | ✅ Yes |
| `-t, --threads` | Number of threads to use | 5 | ❌ No |
| `--timeout` | Request timeout in seconds | 6 | ❌ No |
| `-b, --break` | Stop on first successful find | False | ❌ No |
| `--help` | Show help message | - | ❌ No |

### Examples


# Basic scan with default settings
```bash
python xpanel_tester.py -h targets.txt
```
# Aggressive scan with 20 threads
```bash
python xpanel_tester.py -h targets.txt -t 20 --timeout 3
```
# Stop on first success
```bash
python xpanel_tester.py -h targets.txt -b
```
# Custom timeout
```bash
python xpanel_tester.py -h targets.txt --timeout 10
```
### Input File Format
Create a text file with one hostname/IP per line:
```
192.168.1.1:8080

example.com:80

10.0.0.1:443
```

## 📁 Output Files

The tool generates several output files:

| File | Description |
|------|-------------|
| `hit.txt` | Successfully compromised XPanel instances |
| `wrong_pass.txt` | Instances where login failed (non-default credentials) |
| `FinalCredentials.txt` | Final list of valid panels found |

## 🎨 Color Coding

| Color | Meaning |
|-------|---------|
| 🟢 Green | Success - Panel hacked |
| 🟡 Yellow | Login failed (wrong credentials) |
| 🔴 Red | Timeout/Connection error |
| 🟣 Magenta | Panel not detected |

## 🔐 Authentication

The tool includes built-in password protection. Default password is `s3nat0r!@123`. Users have 3 attempts to enter the correct password.

## ⚙️ How It Works

1. **Input Processing**: Reads target hostnames from specified file
2. **Thread Management**: Creates configurable number of worker threads
3. **Request Handling**: Sends POST requests with default credentials
4. **Response Analysis**: Parses HTML titles to identify XPanel instances
5. **Result Logging**: Automatically categorizes and saves findings

## 📊 Detection Logic

The tool identifies XPanel instances by checking page titles:
- **Success**: Title = "Xpanel" (vulnerable to default credentials)
- **Failed**: Title = "Login | XPanel" (non-default credentials)
- **Unknown**: Other titles or errors

## 🛡️ Security Recommendations

For System Administrators:
- Always change default credentials immediately after installation
- Implement strong password policies
- Regular security audits
- Monitor access logs for suspicious activities
- Keep systems updated with latest security patches

## ⚖️ Legal Compliance

This tool should only be used in compliance with:
- Computer Fraud and Abuse Act (CFAA)
- General Data Protection Regulation (GDPR)
- Local cybersecurity laws
- Your organization's security policies
- Written authorization from system owners

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows ethical guidelines
- Features focus on security improvement
- Documentation is updated
- No encouragement of illegal activities

## 📝 License

This project is licensed for educational and professional security testing purposes only.

## 📞 Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Contact the development team
- Check documentation first

## ⭐ Acknowledgments

- Security community for best practices
- Open-source contributors
- Ethical hacking guidelines

---

**REMEMBER: With great power comes great responsibility! Always stay ethical and legal!** 🔐
