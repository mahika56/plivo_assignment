from flask import Flask, request, jsonify, send_from_directory
import plivo
import os
from ivr import ivr_level1_blueprint, ivr_level2_blueprint, ivr_action_blueprint

app = Flask(__name__)

AUTH_ID = "MANZJJOGRLNZK0ZMZIMM"
AUTH_TOKEN = "NmU2ZmRhMjYtOTE1OS00YWRiLWJlNmEtNTIxYzUy"
FROM_NUMBER = "14692463987"

client = plivo.RestClient(auth_id=AUTH_ID, auth_token=AUTH_TOKEN)

app.register_blueprint(ivr_level1_blueprint)
app.register_blueprint(ivr_level2_blueprint)
app.register_blueprint(ivr_action_blueprint)

@app.route("/make_call", methods=["POST"])
def make_call():
    data = request.json
    to_number = data.get("to")
    try:
        response = client.calls.create(
            from_=FROM_NUMBER,
            to_=to_number,
            answer_url="https://fattier-unindigenously-audrea.ngrok-free.dev/ivr/level1",
            answer_method="GET",
        )
        return jsonify({"status": "success", "call_uuid": response["request_uuid"]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/script.js")
def script():
    return send_from_directory(os.getcwd(), "script.js")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
