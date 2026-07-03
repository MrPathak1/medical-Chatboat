import webbrowser
import platform
import os

def emergency_call():
    emergency_number = "112"  # India’s general emergency number

    if platform.system() == "Windows":
        os.system(f"start tel:{emergency_number}")
    elif platform.system() == "Darwin":  # macOS
        os.system(f"open tel://{emergency_number}")
    else:  # Linux
        webbrowser.open(f"tel:{emergency_number}")
