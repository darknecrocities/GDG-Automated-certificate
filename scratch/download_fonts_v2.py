import requests
import os

os.makedirs("assets/fonts", exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

urls = {
    "Inter-Bold.ttf": "https://github.com/rsms/inter/blob/master/docs/font-files/Inter-Bold.ttf?raw=true",
    "Inter-Regular.ttf": "https://github.com/rsms/inter/blob/master/docs/font-files/Inter-Regular.ttf?raw=true"
}

for name, url in urls.items():
    print(f"Downloading {name}...")
    r = requests.get(url, headers=headers, allow_redirects=True)
    if r.status_code == 200:
        with open(f"assets/fonts/{name}", "wb") as f:
            f.write(r.content)
        print(f"Successfully downloaded {name} ({len(r.content)} bytes)")
    else:
        print(f"Failed to download {name}: {r.status_code}")
