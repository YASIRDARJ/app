from flask import Flask, request, jsonify, render_template
import random
import time, os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# Mock Stripe API (بديل آمن)
@app.route("/mock_stripe")
def mock_stripe():
    card = request.args.get("cc", "")
    time.sleep(0.8)

    if random.random() < 0.25:
        return jsonify({
            "By": "@PR_7N",
            "Payment gateway": "STRIPE AUTHE",
            "Response": "Approved",
            "success": True
        })

    return jsonify({
        "By": "@PR_7N",
        "Payment gateway": "STRIPE AUTHE",
        "Response": "Token has expired",
        "success": False
    })

@app.route("/check", methods=["POST"])
def check_cards():
    data = request.get_json()
    cards = data.get("cards", [])

    live = approved = declined = 0
    declined_msgs = []
    approved_msgs = []

    for card in cards:
        card = card.strip()
        if not card:
            continue

        res = app.test_client().get(f"/mock_stripe?cc={card}").get_json()

        if res["success"]:
            live += 1
            approved += 1
            approved_msgs.append(f"{card} ➜ Approved")
        else:
            declined += 1
            declined_msgs.append(f"{card} ➜ {res['Response']}")

    return jsonify({
        "live": live,
        "approved": approved,
        "declined": declined,
        "approved_msgs": approved_msgs,
        "declined_msgs": declined_msgs
    })

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
