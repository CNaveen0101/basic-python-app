from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message="Hello Naveen")

@app.route("/health")
def health():
    return jsonify(status="OK")

if __name__ == "__main__":
    # Run on all network interfaces for Docker
    app.run(host="0.0.0.0", port=5000)
