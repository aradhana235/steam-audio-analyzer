import requests

url = "http://localhost:5000/analyze-audio"
payload = {
    "audio_url": "https://filesamples.com/samples/audio/mp3/sample1.mp3",
    "token": "txmQsJlh7NIuKyPF3tn3"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print("Status:", response.status_code)
print("Response:", response.text)
