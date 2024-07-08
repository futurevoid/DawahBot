import requests
from bs4 import BeautifulSoup

url = "https://anasalafy.com/ar/109695"
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all image tags
images = soup.find_all('img')

# Loop through images and find one in the /uploads/thumbnails/big/ directory
for img in images:
    src = img.get('src')
    if '/uploads/thumbnails/big/' in src and 'logo' not in src:
        # Prepend the base URL if the src is a relative path
        if not src.startswith('http'):
            src = f"https://anasalafy.com{src}"
        print(src)
        # Download the image
        img_response = requests.get(src)
        with open('image.jpg', 'wb') as file:
            file.write(img_response.content)
        break