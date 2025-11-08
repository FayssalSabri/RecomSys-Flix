"""
Script de lancement de l'application Streamlit
"""
import subprocess
import sys
import os

def main():
    print(" Lancement de RecomSys-Flix Streamlit...")
    
    # Vérifier que Streamlit est installé
    try:
        import streamlit
        print(" Streamlit est installé")
    except ImportError:
        print(" Streamlit n'est pas installé. Installation...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "streamlit"])
    
    # Lancer l'application Streamlit
    streamlit_app_path = os.path.join(os.path.dirname(__file__), "streamlit_app", "main.py")
    
    if os.path.exists(streamlit_app_path):
        print(f" Lancement de {streamlit_app_path}")
        subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_app_path])
    else:
        print(" Fichier Streamlit non trouvé")
        print(" Assurez-vous que la structure des fichiers est correcte")

if __name__ == "__main__":
    main()