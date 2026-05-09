import requests
import os

os.makedirs("assets/fonts", exist_ok=True)

urls = {
    "Inter-Bold.ttf": "https://github.com/google/fonts/raw/main/ofl/inter/static/Inter-Bold.ttf",
    "Inter-Regular.ttf": "https://github.com/google/fonts/raw/main/ofl/inter/static/Inter-Regular.ttf"
}

for name, url in urls.items():
    print(f"Downloading {name}...")
    r = requests.get(url, allow_redirects=True)
    if r.status_code == 200:
        with open(f"assets/fonts/{name}", "wb") as f:
            f.write(r.content)
        print(f"Successfully downloaded {name}")
    else:
        print(f"Failed to download {name}: {r.status_code}")
