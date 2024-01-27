#!/usr/bin/env python
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import requests
import base64
from datetime import datetime
import time
import json

# Load settings from settings.json
with open("settings.json", "r") as settings_file:
    settings = json.load(settings_file)
    
TELEGRAM_BOT_TOKEN = settings.get("TELEGRAM_BOT_TOKEN", "")
GITHUB_ACCESS_TOKEN = settings.get("GITHUB_ACCESS_TOKEN", "")
OWNER_TELEGRAM_ID = settings.get("OWNER_TELEGRAM_ID", "")
REPO_OWNER = settings.get("REPO_OWNER", "")
REPO_NAME = settings.get("REPO_NAME", "")
FILE_NAME = settings.get("FILE_NAME", "")

# Inisialisasi bot
bot = telebot.TeleBot(settings.get("TELEGRAM_BOT_TOKEN", ""))

# Record the bot start time
bot_start_time = time.time()

# Fungsi untuk menangani perintah '/runtime'
@bot.message_handler(commands=['runtime'])
def runtime(message):

    # Calculate the runtime in seconds
    runtime_seconds = int(time.time() - bot_start_time)

    # Convert seconds to days, hours, minutes, and seconds
    days, remainder = divmod(runtime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Generate the runtime message
    runtime_message = f"Bot Aktif Selama :\n{days} Hari, {hours} Jam, {minutes} Menit, {seconds} Detik."

    # Send the runtime message
    bot.send_message(message.chat.id, runtime_message)
    
# Fungsi untuk membuat tombol inline (lanjutan)
def create_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    register_ip_button = types.InlineKeyboardButton("Register IP", callback_data="register_ip")
    delete_ip_button = types.InlineKeyboardButton("Delete IP", callback_data="delete_ip")
    list_ip_button = types.InlineKeyboardButton("List IP", callback_data="list_ip")
    install_script_button = types.InlineKeyboardButton("Install Script", callback_data="install_script")
    whatsapp_button = types.InlineKeyboardButton("WhatsApp", url="https://wa.me/+6285225416745")
    telegram_button = types.InlineKeyboardButton("Telegram", url="https://t.me/RidwanzSaputra")
    runtime_button = types.InlineKeyboardButton("Runtime", callback_data="runtime_command")

    # Urutan tombol Button
    keyboard.add(register_ip_button, delete_ip_button, list_ip_button, install_script_button, whatsapp_button, telegram_button, runtime_button)
    return keyboard

# Fungsi untuk menangani query inline
@bot.callback_query_handler(func=lambda call: True)
def inline_button_callback(call):
    user_id = call.from_user.id

    if call.data == "register_ip":
        bot.send_message(call.message.chat.id, "Silakan Masukkan IP VPS Yang Ingin Anda Daftarkan.")
        bot.register_next_step_handler(call.message, ask_name_for_registration)
    elif call.data == "delete_ip":
        if str(user_id) == OWNER_TELEGRAM_ID:
            bot.send_message(call.message.chat.id, "Silakan Masukkan Nama Yang Ingin Anda Hapus.")
            bot.register_next_step_handler(call.message, delete_ip_step)
        else:
            bot.send_message(call.message.chat.id, "Maaf, Fitur Ini Hanya Bisa Digunakan Oleh Owner Bot.")
    elif call.data == "install_script":
        bot.send_message(call.message.chat.id, get_installation_text(), parse_mode="Markdown")
    elif call.data == "runtime_command":
        runtime(call.message)
    elif call.data == "list_ip":
        list_registered_ips(call.message)

# Fungsi untuk menampilkan daftar IP yang terdaftar
def list_registered_ips(message):
    # Dapatkan konten file ipvps
    content_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"
    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    existing_content = requests.get(content_url, headers=headers).json().get("content", "")
    
    if existing_content:
        existing_content = base64.b64decode(existing_content).decode()
        entries = [line.split() for line in existing_content.split('\n') if line.startswith("###")]

        if entries:
            # Sort entries by date
            sorted_entries = sorted(entries, key=lambda entry: datetime.strptime(entry[2], '%Y-%m-%d'))
            ips_message = "\n".join([f"{index + 1}. {entry[1]} {entry[2]} {entry[3]}" for index, entry in enumerate(sorted_entries)])
            bot.send_message(message.chat.id, f"Daftar IP Yang Terdaftar :\n{ips_message}")
        else:
            bot.send_message(message.chat.id, "Belum ada IP yang terdaftar.")

# Fungsi untuk menangani query inline
@bot.callback_query_handler(func=lambda call: True)
def inline_button_callback(call):
    if call.data == "register_ip":
        bot.send_message(call.message.chat.id, "Silakan Masukan IP VPS Yang Ingin Anda Daftarkan.")
        bot.register_next_step_handler(call.message, ask_name_for_registration)
    elif call.data == "delete_ip":
        bot.send_message(call.message.chat.id, "Silakan Masukan Nama Yang Ingin Anda Hapus.")
        bot.register_next_step_handler(call.message, delete_ip_step)
    elif call.data == "install_script":
        bot.send_message(call.message.chat.id, get_installation_text(), parse_mode="Markdown")

# Fungsi untuk mendapatkan teks instalasi
def get_installation_text():
    return """
```
apt update && apt upgrade -y --fix-missing && update-grub && sleep 2 && apt -y install xxd && apt install -y bzip2 && apt install -y wget && apt install -y curl && reboot
```

```
sysctl -w net.ipv6.conf.all.disable_ipv6=1 && sysctl -w net.ipv6.conf.default.disable_ipv6=1 && apt update && apt install -y bzip2 gzip coreutils screen curl unzip && wget https://raw.githubusercontent.com/RidwanzAnphelibelll/v6/main/setup.sh && chmod +x setup.sh && sed -i -e 's/\r$//' setup.sh && screen -S setup ./setup.sh
```

**•ᴘᴇʀʜᴀᴛɪᴀɴ•**\n\n**sᴇʙᴇʟᴜᴍ ɪɴsᴛᴀʟʟ sᴄʀɪᴘᴛ ᴅɪᴀᴛᴀs ᴡᴀᴊɪʙ ʀᴇɢɪsᴛᴇʀ ɪᴘ ᴠᴘs ᴛᴇʀʟᴇʙɪʜ ᴅᴀʜᴜʟᴜ.**
"""

# Fungsi untuk menangani perintah '/start'
@bot.message_handler(commands=['start'])
def start(message):
    # Mention the user's Telegram username
    username_mention = f"@{message.from_user.username}" if message.from_user.username else "User"
    
    # Send the welcome message with the mentioned username
    welcome_message = f"ʜᴀʟʟᴏ! {username_mention}👋\nsɪʟᴀʜᴋᴀɴ ᴋʟɪᴋ ᴛᴏᴍʙᴏʟ ʙᴜᴛᴛᴏɴ ᴅɪ ʙᴀᴡᴀʜ ɪɴɪ ᴜɴᴛᴜᴋ ᴍᴇɴɢᴀᴋsᴇs ᴍᴇɴᴜ."
    bot.send_message(message.chat.id, welcome_message, reply_markup=create_inline_keyboard())

# Fungsi untuk menangani query inline
@bot.callback_query_handler(func=lambda call: True)
def inline_button_callback(call):
    if call.data == "register_ip":
        bot.send_message(call.message.chat.id, "Silakan Masukan IP VPS Yang Ingin Anda Daftarkan.")
        bot.register_next_step_handler(call.message, ask_name_for_registration)
    elif call.data == "delete_ip":
        bot.send_message(call.message.chat.id, "Silakan Masukan Nama Yang Ingin Anda Hapus.")
        bot.register_next_step_handler(call.message, delete_ip_step)

# Fungsi untuk menanyakan nama sebelum mendaftarkan IP
def ask_name_for_registration(message):
    ip_address = message.text

    if ip_address:
        bot.send_message(message.chat.id, "Silakan Masukan Nama IP Yang Ingin Anda Daftarkan.")
        bot.register_next_step_handler(message, lambda m: ask_date_for_registration(m, ip_address))
    else:
        bot.send_message(message.chat.id, "Silakan Masukan IP VPS Yang Ingin Anda Daftarkan.")

# Fungsi untuk menanyakan tanggal sebelum mendaftarkan IP
def ask_date_for_registration(message, ip_address):
    name = message.text

    if name:
        bot.send_message(message.chat.id, "Silakan Masukan Tanggal Dengan Format YYYY-MM-DD : \n(Contoh : 2025-02-12).")
        bot.register_next_step_handler(message, lambda m: register_ip_step(m, ip_address, name))
    else:
        bot.send_message(message.chat.id, "Silakan Masukan Nama IP Yang Ingin Anda Daftarkan.")

# Langkah selanjutnya untuk mendaftarkan IP dengan nama dan tanggal yang ditentukan
def register_ip_step(message, ip_address, name):
    date_str = message.text

    try:
        # Konversi tanggal ke format yang diinginkan
        registration_date = datetime.strptime(date_str, "%Y-%m-%d").strftime('%Y-%m-%d')
    except ValueError:
        bot.send_message(message.chat.id, "Format Tanggal Tidak Valid. Gunakan Format YYYY-MM-DD (contoh: 2025-02-12).")
        return

    # Dapatkan SHA dari file ipvps
    sha_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"
    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    response = requests.get(sha_url, headers=headers)
    sha = response.json().get("sha", "")

    # Dapatkan konten file ipvps yang sudah ada
    content_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"
    existing_content = requests.get(content_url, headers=headers).json().get("content", "")
    
    # Cek apakah konten sudah ada atau belum
    if existing_content:
        existing_content = base64.b64decode(existing_content).decode()

    # Buat string dengan format ### {nama} {tanggal} {ip_address}
    new_entry = f"### {name} {registration_date} {ip_address}"

    # Tambahkan IP baru ke konten yang sudah ada
    new_content = f"{existing_content}\n{new_entry}" if existing_content else new_entry

    # Konversi teks ke format Base64
    content_base64 = base64.b64encode(new_content.encode()).decode()

    # Tambahkan IP ke file ipvps di repositori GitHub
    commit_message = f"Register IP: {ip_address}"
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"

    headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
    payload = {"branch": "main", "content": content_base64, "message": commit_message, "sha": sha}
    response = requests.put(url, headers=headers, json=payload)

    if response.status_code == 200:
        bot.send_message(message.chat.id, f"IP {ip_address} Berhasil Didaftarkan Ke GitHub!")
    else:
        bot.send_message(message.chat.id, f"Terjadi kesalahan: {response.status_code}, {response.text}")

# Langkah selanjutnya untuk menghapus IP berdasarkan nama
def delete_ip_step(message):
    name = message.text

    if name:
        # Dapatkan SHA dari file ipvps
        sha_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"
        headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
        response = requests.get(sha_url, headers=headers)
        sha = response.json().get("sha", "")

        # Dapatkan konten file ipvps yang sudah ada
        content_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"
        existing_content = requests.get(content_url, headers=headers).json().get("content", "")
        existing_content = base64.b64decode(existing_content).decode()

        # Hapus entri IP berdasarkan nama
        updated_content = '\n'.join(line for line in existing_content.split('\n') if name not in line)

        # Konversi teks ke format Base64
        content_base64 = base64.b64encode(updated_content.encode()).decode()

        # Update file ipvps di repositori GitHub
        commit_message = f"Delete IP: {name}"
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/contents/{FILE_NAME}"

        headers = {"Authorization": f"token {GITHUB_ACCESS_TOKEN}"}
        payload = {"branch": "main", "content": content_base64, "message": commit_message, "sha": sha}
        response = requests.put(url, headers=headers, json=payload)

        if response.status_code == 200:
            bot.send_message(message.chat.id, f"IP Dengan Nama {name} Berhasil Dihapus Dari GitHub!")
        else:
            bot.send_message(message.chat.id, f"Terjadi kesalahan: {response.status_code}, {response.text}")
    else:
        bot.send_message(message.chat.id, "Silakan Masukan Nama IP Yang Ingin Anda Hapus.")

# Menjalankan bot
if __name__ == "__main__":
    try:
        # Tampilkan pesan sukses terhubung dengan server
        print("\033[92mBot Berhasil Terhubung Ke Server!\033[0m")
        # Start polling
        bot.polling()
    except Exception as e:
        # Tampilkan pesan error jika terjadi masalah
        print(f"\033[91mError: {e}\033[0m")  