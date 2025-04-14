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
        return (
            "⚠️ Kondisi udara saat ini panas dan lembap. "
            "Suhu di atas 30°C mempercepat penguapan air dan membuat udara terasa sangat gerah. "
            "Kelembapan tinggi (di atas 70%) membuat keringat sulit menguap, menyebabkan tubuh tidak bisa mendinginkan diri dengan baik. "
            "Kondisi seperti ini meningkatkan risiko kelelahan panas, dehidrasi, dan pertumbuhan mikroorganisme seperti bakteri dan jamur di udara. "
            "Ini bisa memperburuk polusi udara dan menyebabkan gangguan pernapasan seperti ISPA, terutama pada anak-anak, lansia, dan penderita asma.\n\n"
            "👉 Disarankan untuk **berpindah ke dalam ruangan** yang sejuk, bersih, dan berventilasi baik — seperti ruangan ber-AC atau menggunakan air purifier. "
            "Kurangi aktivitas fisik di luar ruangan dan perbanyak minum air putih."
        )
    elif temp < 20:
        return (
            "🌬️ Udara saat ini tergolong dingin dengan suhu di bawah 20°C. "
            "Suhu rendah bisa memicu penyempitan saluran pernapasan dan menurunkan daya tahan tubuh. "
            "Jika kelembapan juga rendah, udara akan terasa lebih kering dan bisa menyebabkan iritasi pada hidung dan tenggorokan.\n\n"
            "👉 Jika merasa tidak nyaman, segera berpindah ke ruangan hangat dan lembap, seperti menggunakan humidifier. "
            "Kenakan pakaian hangat dan hindari paparan langsung ke udara dingin terlalu lama."
        )
    else:
        return (
            "✅ Kondisi udara saat ini tergolong stabil dan nyaman. "
            "Suhu dan kelembapan berada dalam rentang ideal bagi kesehatan (sekitar 20–30°C dan kelembapan 40–60%). "
            "Risiko terhadap kesehatan pernapasan relatif rendah, namun tetap waspada terhadap perubahan mendadak cuaca dan kualitas udara.\n\n"
            "👉 Meski stabil, pastikan ruangan tetap memiliki sirkulasi udara yang baik, dan hindari paparan polusi dalam jangka panjang."
        )


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