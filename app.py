from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/route", methods=["POST"])
def get_route():
    data = request.json
    start = data["start"]
    end = data["end"]

    url = (
        f"https://router.project-osrm.org/route/v1/foot/"
        f"{start['lon']},{start['lat']};"
        f"{end['lon']},{end['lat']}"
        f"?overview=full&geometries=polyline"
    )

    print("Request URL:", url)

    res = requests.get(url).json()
    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True)
