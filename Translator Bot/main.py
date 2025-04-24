import discord
from discord.ext import commands
from discord.ui import Button, View
from googletrans import Translator
from dotenv import load_dotenv
import os
import requests
from keep_alive import keep_alive  # Import webserver

# Intents setup
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True  # Enable reaction events
bot = commands.Bot(command_prefix="!", intents=intents)

translator = Translator()
user_messages = {}

languages = {
    "en English": "en",
    "es Spanish": "es",
    "🇫🇷 French": "fr",
    "🇷🇺 Russian": "ru",
    "🇯🇵 Japanese": "ja",
}

# Role name to language code mapping
role_lang_map = {
    "English": "en",
    "Española": "es",
    "Français": "fr",
    "русский": "ru",
    "日本語": "ja",
}


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

    # Set bot bio/about me
    try:
        headers = {
            "Authorization": f"Bot {os.environ['DISCORD_TOKEN']}",
            "Content-Type": "application/json"
        }

        data = {
            "bio":
            "🌐 I'm your personal translator bot. Select a language to translate any message!"
        }

        response = requests.patch("https://discord.com/api/v10/users/@me",
                                  headers=headers,
                                  json=data)

        if response.status_code == 200:
            print("✅ Bot bio updated successfully!")
        else:
            print("❌ Failed to update bio:", response.status_code,
                  response.text)
    except Exception as e:
        print("❌ Error updating bot bio:", str(e))


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    user_messages[message.author.id] = message.content

    view = View()
    for label, lang_code in languages.items():
        button = Button(label=label,
                        style=discord.ButtonStyle.primary,
                        custom_id=lang_code)
        button.callback = button_callback
        view.add_item(button)

    await message.channel.send(
        "🌐 Select a language to translate your last message:", view=view)
    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if str(reaction.emoji) != "❤️":
        return

    message = reaction.message
    original_text = message.content

    # Get the user's language from their roles
    lang_code = None
    for role in user.roles:
        if role.name in role_lang_map:
            lang_code = role_lang_map[role.name]
            break

    if not lang_code:
        try:
            await user.send("⚠️ You don't have a language role set.")
        except:
            pass
        return

    translated = await translator.translate(original_text, dest=lang_code)

    try:
        await user.send(
            f"**{message.author.display_name} said ({lang_code}):** {translated.text}"
        )
    except:
        print(f"❌ Couldn't DM {user.display_name}")


async def button_callback(interaction: discord.Interaction):
    lang_code = interaction.data['custom_id']
    user_id = interaction.user.id

    original_text = user_messages.get(user_id)
    if not original_text:
        await interaction.response.send_message(
            "⚠️ No recent message found to translate.", ephemeral=True)
        return

    translated = await translator.translate(original_text, dest=lang_code)
    await interaction.response.send_message(
        f"**{interaction.user.display_name} said ({lang_code}):** {translated.text}",
        ephemeral=True)


# 🟢 Start web server & bot
if __name__ == "__main__":
    load_dotenv()
    keep_alive()
    bot.run(os.environ["DISCORD_TOKEN"])
