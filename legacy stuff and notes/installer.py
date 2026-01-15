import subprocess
import sys

def check_python():
    try:
        subprocess.run([sys.executable, "--version"], check=True)
        return True
    except Exception:
        return False

def install_pyqt6():
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.run([sys.executable, "-m", "pip", "install", "pyqt6"])

if __name__ == "__main__":
    if not check_python():
        print("Python is not installed. Please install Python 3.10+ and rerun.")
        input("Press Enter to exit...")
        sys.exit(1)
    install_pyqt6()
    print("PyQt6 installed. You can now run Warhammer Clock.")
    input("Press Enter to launch the app...")
    subprocess.run([sys.executable, "warhammerclock.py"])
