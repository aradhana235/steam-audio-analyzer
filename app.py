from flask import Flask, request
import librosa
import numpy as np
import requests
import soundfile as sf
import urllib.request
import io

app = Flask(__name__)

def classify_audio(y, sr):
    zcr = np.mean(librosa.feature.zero_crossing_rate(y))
    centroid = np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr))

    if zcr < 0.01 and centroid < 500 and mfcc < 30:
        return "blocked"
    elif zcr > 0.1 or centroid > 2500 or mfcc > 100:
        return "leak"
    else:
        return "normal"

@app.route('/analyze-audio', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('audio_url')
    token = data.get('token')

    try:
        req = urllib.request.Request(
            url,
            headers={"Referer": "https://thingsboard.cloud"}
        )
        with urllib.request.urlopen(req) as response:
            audio_data = response.read()

        y, sr = librosa.load(io.BytesIO(audio_data), sr=None)
        label = classify_audio(y, sr)

        tb_url = f"https://thingsboard.cloud/api/v1/{token}/telemetry"
        requests.post(tb_url, json={"sound_type": label})

        return {"status": "ok", "result": label}
    except Exception as e:
        return {"error": str(e)}, 500
