from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api")
def api():
    data = {
        "name": "Flask API",
        "status": "ok"
    }
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)