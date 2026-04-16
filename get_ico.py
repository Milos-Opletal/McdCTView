import os
import requests

def download_icon():
    # Fetching directly from SimpleIcons
    url = "https://cdn.simpleicons.org/mcdonalds/ff9614"
    print(f"Fetching vector icon from {url}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Ensure the static directory exists
        os.makedirs("static", exist_ok=True)
        
        # We drop the .ico conversion entirely! All modern web browsers natively support scalable .svg favicons.
        file_path = os.path.join("static", "favicon.svg")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
            
        print(f"Success! Icon downloaded and saved to: {file_path}")
        print("Your browser will automatically scale this perfectly without needing any Pillow conversion overhead.")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to download icon: {e}")

if __name__ == "__main__":
    download_icon()
