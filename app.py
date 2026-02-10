from flask import Flask, request, jsonify, render_template
import os
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/check", methods=["POST"])
def check_cards():
    data = request.get_json()
    cards = data.get("cards", [])
    live = approved = declined = 0
    for c in cards:
        import random
        r = random.random()
        if r < 0.2:
            live += 1
            approved += 1
        else:
            declined += 1
    return jsonify({"live": live, "approved": approved, "declined": declined})

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
