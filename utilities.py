import os
import subprocess

def clear_screen():
    """
    Clears the terminal screen  for a clean look.
    """
    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)