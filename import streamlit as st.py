import streamlit as st
import requests

st.title("hello, streamlit")
st.write("ini adalah web untuk membuat app")
# === KONFIGURASI UBIDOTS ===
UBIDOTS_TOKEN = "BBUS-d7C5rsZYPefWzzHuhGNd0t0eYqwpoF"
DEVICE_LABEL = "hiruppintar"
VARIABLES = ["temperature", "humidity"]

def get_latest_data():
    base_url = f"https://industrial.api.ubidots.com/api/v1.6/devices/{DEVICE_LABEL}/"
    headers = {"X-Auth-Token": UBIDOTS_TOKEN}
    result = {}

    for var in VARIABLES:
        url = base_url + var + "/lv"
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            result[var] = float(r.text)
        else:
            result[var] = None
    return result

# === LOGIKA KETERANGAN AI (dummy manual atau nanti sambung Gemini) ===
def get_ai_keterangan(temp, hum):
    if temp > 30 and hum > 70:
        return "Udara panas dan lembap. Risiko tinggi untuk penderita ISPA."
    elif temp < 20:
        return "Udara dingin, jaga kesehatan!"
    else:
        return "Udara cukup stabil."

# === STREAMLIT UI ===
st.title("Dashboard Hirup Pintar")

data = get_latest_data()
temperature = data["temperature"]
humidity = data["humidity"]

if temperature and humidity:
    st.metric("Suhu", f"{temperature} °C")
    st.metric("Kelembaban", f"{humidity} %")

    # Tampilkan Keterangan AI
    keterangan = get_ai_keterangan(temperature, humidity)
    st.info(keterangan)
else:
    st.warning("Gagal mengambil data dari Ubidots.")