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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
