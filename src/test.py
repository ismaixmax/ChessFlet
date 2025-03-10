import os
import requests

# Define the URLs for the chess piece images
piece_urls = {
    "wp": "https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg",
    "wn": "https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg",
    "wb": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Chess_blt45.svg",
    "wr": "https://upload.wikimedia.org/wikipedia/commons/7/72/Chess_rlt45.svg",
    "wq": "https://upload.wikimedia.org/wikipedia/commons/1/15/Chess_qlt45.svg",
    "wk": "https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_klt45.svg",
    "bp": "https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg",
    "bn": "https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg",
    "bb": "https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg",
    "br": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg",
    "bq": "https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg",
    "bk": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg",
}

# Create the images directory if it doesn't exist
os.makedirs("images", exist_ok=True)

# Download and save each image
for piece, url in piece_urls.items():
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"images/{piece}.png", "wb") as file:
            file.write(response.content)
        print(f"Downloaded {piece}.png")
    else:
        print(f"Failed to download {piece}.png")

print("All images downloaded.")