from flask import Flask, request, jsonify
import time

app = Flask(__name__)

# Memoriaban taroljuk az uzeneteket (ha ujraindulsz a Renderen, ez torlodik)
messages = []

@app.route('/')
def home():
    return "A Cherax Chat Szerver fut! Mozes a vonalban."

# --- Uzenetek lekerese (Ezt hivja a Cherax) ---
@app.route('/get-from-discord', methods=['GET'])
def get_discord_messages():
    # Visszakuldjuk az utolso 20 uzenetet (hogy ne legyen tul sok adat)
    return jsonify(messages[-20:])

# --- Uzenet kuldese (Ezt kuldi a Cherax) ---
@app.route('/send-to-discord', methods=['POST'])
def send_discord_message():
    data = request.json
    
    # Ellenorizzuk, hogy van-e adat
    if not data or 'name' not in data or 'text' not in data:
        return jsonify({"error": "Hianyos adat"}), 400

    # Hozzaadjuk a listahoz
    new_msg = {
        "name": data['name'],
        "text": data['text'],
        "timestamp": time.time()
    }
    messages.append(new_msg)
    
    # Memoriavedelem: csak az utolso 50 uzenetet taroljuk
    if len(messages) > 50:
        messages.pop(0)

    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
