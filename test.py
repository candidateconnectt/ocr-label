import requests

url = "https://ocr-label.vercel.app/ocr"
drive_url = "https://drive.google.com/uc?export=download&id=1bjdJOKHTqTVs0m_fF8uSb1UR8CGcd9hX"

data = {"url": drive_url}
response = requests.post(url, data=data)

print("Status:", response.status_code)
print("Response:", response.json())
