# Free to use lightweight Calculator for everyone!

## Calculator-win Dark mode

<img width="170" height="200" alt="Calculator-win-dark" src="https://github.com/user-attachments/assets/b83a6ad1-6d68-4a28-ad72-b53affe64ada" /><br>

## Calculator-win Light mode

<img width="170" height="200" alt="Calculator-win-light" src="https://github.com/user-attachments/assets/03f772d2-8d63-4eb8-83ec-4875f2c9562f" /><br>

## Calculator-linux Dark mode

<img width="170" height="200" alt="Calculator-linux-dark" src="https://github.com/user-attachments/assets/0db1a8ff-37dd-4c67-9fd7-233cb2cd080c" /><br>

## Calculator-linux Light mode

<img width="170" height="200" alt="Calculator-linux-light" src="https://github.com/user-attachments/assets/3eb1aabc-8460-4e88-ad78-81165071109e" />

# Rebuild the calculator

## Requirements (Linux)

- Debian-based distro / Windows Subsystem for Linux
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
