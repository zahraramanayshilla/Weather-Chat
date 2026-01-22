from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")


def get_weather(city):
    try:
        url = (
            "http://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric&lang=id"
        )
        data = requests.get(url, timeout=5).json()

        if data.get("cod") != 200:
            return f" Kota tidak ditemukan."

        return (
            f"🌤️ Cuaca di {city.title()}<br>"
            f"Suhu: {data['main']['temp']} °C<br>"
            f"Kelembapan: {data['main']['humidity']}%<br>"
            f"Kondisi: {data['weather'][0]['description']}"
        )
    except:
        return " Gagal mengambil data cuaca."


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    msg = request.json["message"].lower()

    if msg in ["halo", "hai", "hi"]:
        return jsonify(
            reply="Halo <br>Pilih perintah:<br>- ketik <b>cuaca</b><br>- ketik <b>help</b>"
        )

    if msg == "help":
        return jsonify(
            reply="Perintah:<br>• cuaca &lt;nama_kota&gt;<br>• halo<br>• help"
        )

    if msg.startswith("cuaca"):
        city = msg.replace("cuaca", "").strip()
        if not city:
            return jsonify(reply="Nama kota tidak boleh kosong.")
        return jsonify(reply=get_weather(city))

    return jsonify(reply=" Perintah tidak dikenali. Ketik <b>help</b>.")


if __name__ == "__main__":
    app.run(debug=True)
