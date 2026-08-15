# Free to use lightweight Calculator for everyone!
# Rebuild the calculator
## Requirements (Linux)
- Debian based distro / Windows Subsystem for Linux
- Python3
- python3-tk
- dpkg-dev
## Requirements (Windows)
- Python3 from https://python.org/
- Visual Studio Code, Pycharm or Windows terminal
- PyInstaller && auto-py-to-exe
### Rebuilding Tutorial
1. **On Windows**
   - Use **PyInstaller**: `pip install pyinstaller`
   - Or use **auto-py-to-exe**: `pip install auto-py-to-exe`

2. **On Debian-based distros**  
   (for example: Ubuntu, Zorin OS, Linux Mint, etc...)
   a. Use the same structure as the `Calculator-source-deb` folder.  
   b. Run:

   
```bash
   dpkg-deb --build FILE_NAME
```
### Don't forget to credit me!
