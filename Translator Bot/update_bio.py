import requests
import os

# Replace with your bot's token
token = os.environ["DISCORD_TOKEN"]

# Your new bio
bio_text = "🌐 I translate messages in your language!"

url = "https://discord.com/api/v10/users/@me"

headers = {
    "Authorization": f"Bot {token}",
    "Content-Type": "application/json"
}

data = {
    "bio": bio_text
}

response = requests.patch(url, headers=headers, json=data)

if response.status_code == 200:
    print("✅ Bot bio updated successfully!")
else:
    print(f"❌ Failed to update bio: {response.status_code}")
    print(response.text)
