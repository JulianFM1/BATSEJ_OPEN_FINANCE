import os
import sys
import subprocess

def install_packages():
    """Instala las librerías necesarias en Windows o Linux"""
    try:
        # Detectar sistema operativo
        if sys.platform.startswith("win"):
            print("Detectado: Windows")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        elif sys.platform.startswith("linux"):
            print("Detectado: Linux")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            print("Sistema operativo no soportado")
            return
        
        print("Instalación completada con éxito.")
    except Exception as e:
        print(f"Error en la instalación: {e}")

if __name__ == "__main__":
    install_packages()
