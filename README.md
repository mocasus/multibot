<div align="center">
  <img src="assets/logo-v1-robot.png" width="128" height="128" alt="MultiBot Logo">
  <h1>🤖 MultiBot</h1>
  <p><b>Telegram multi-tool bot</b> — download, QR, shortlink, sticker, cuaca, kalkulator.</p>

  <p>
    <a href="https://github.com/mocasus/multibot/releases"><img src="https://img.shields.io/badge/version-v1.0-181717?style=flat-square&logo=github" alt="Version"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License"></a>
    <img src="https://img.shields.io/badge/python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/code%20style-ruff-30173D?style=flat-square&logo=ruff" alt="Ruff">
    <img src="https://img.shields.io/badge/LOC-447-181717?style=flat-square" alt="LOC">
  </p>

  <p>
    <a href="https://github.com/mocasus/multibot/stargazers"><img src="https://img.shields.io/github/stars/mocasus/multibot?style=flat-square&cacheSeconds=86400" alt="Stars"></a>
    <a href="https://github.com/mocasus/multibot/network/members"><img src="https://img.shields.io/github/forks/mocasus/multibot?style=flat-square&cacheSeconds=86400" alt="Forks"></a>
    <a href="https://github.com/mocasus/multibot/issues"><img src="https://img.shields.io/github/issues/mocasus/multibot?style=flat-square&cacheSeconds=86400" alt="Issues"></a>
    <img src="https://img.shields.io/github/last-commit/mocasus/multibot?style=flat-square&cacheSeconds=86400" alt="Last Commit">
    <img src="https://img.shields.io/github/repo-size/mocasus/multibot?style=flat-square&cacheSeconds=86400" alt="Repo Size">
  </p>

  <p>
    <a href="#-features"><img src="https://img.shields.io/badge/Features-✨-brightgreen?style=flat-square" alt="Features"></a>
    <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick_Start-🚀-orange?style=flat-square" alt="Quick Start"></a>
    <a href="#-commands"><img src="https://img.shields.io/badge/Commands-📋-blue?style=flat-square" alt="Commands"></a>
    <a href="#-deploy"><img src="https://img.shields.io/badge/Deploy-🖥-red?style=flat-square" alt="Deploy"></a>
    <a href="#-project-structure"><img src="https://img.shields.io/badge/Structure-📁-gray?style=flat-square" alt="Structure"></a>
  </p>
</div>

---

## ✨ Features

- 📥 **Video Downloader** — Download video dari Instagram, TikTok, YouTube dengan `/dl`
- 🔳 **QR Code Generator** — Generate QR code langsung di chat dengan `/qr`
- 🔗 **URL Shortener** — Pendein URL via TinyURL / is.gd dengan `/short`
- 🖼 **Sticker Converter** — Konversi foto ↔ stiker dengan `/sticker` & `/toimg`
- 🌤 **Cek Cuaca** — Info cuaca real-time dengan `/cuaca [kota]`
- 🧮 **Kalkulator** — Hitung ekspresi matematika dengan `/calc`

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/mocasus/multibot.git
cd multibot

# Setup venv + install
python3 -m venv venv
./venv/bin/pip install -r requirements.txt

# Konfigurasi
cp .env .env.local
# Edit .env.local — isi BOT_TOKEN dari BotFather

# Jalankan
./venv/bin/python3 bot.py
```

---

## 📋 Commands

| Command | Fungsi | Contoh |
|---------|--------|--------|
| `/start` | Info bot & welcome | `/start` |
| `/help` | List semua command | `/help` |
| `/dl [url]` | Download video | `/dl https://instagram.com/p/...` |
| `/qr [teks]` | Generate QR code | `/qr https://github.com` |
| `/short [url]` | Shorten URL | `/short https://example.com/very/long` |
| `/sticker` | Foto → Stiker (reply foto) | Reply foto + `/sticker` |
| `/toimg` | Stiker → PNG (reply stiker) | Reply stiker + `/toimg` |
| `/cuaca [kota]` | Cek cuaca | `/cuaca Jakarta` |
| `/calc [ekspr]` | Kalkulator | `/calc sqrt(144) + 2^3` |

---

## 🖥 Deploy

### systemd (Linux VPS)

```bash
sudo cp multibot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now multibot
sudo systemctl status multibot
```

### Docker

```bash
docker build -t multibot .
docker run -d --env-file .env --name multibot multibot
```

---

## ⚙️ Konfigurasi

Edit `.env`:

| Variable | Required | Deskripsi |
|----------|----------|-----------|
| `BOT_TOKEN` | ✅ | Token dari [@BotFather](https://t.me/BotFather) |
| `WEATHER_API_KEY` | ❌ | API key [OpenWeatherMap](https://openweathermap.org/api) (untuk `/cuaca`) |
| `ADMIN_IDS` | ❌ | Telegram user ID admin (pisah koma) |

---

## 📁 Project Structure

```
multibot/
├── bot.py                  # Entry point
├── config.py               # Env loader
├── requirements.txt        # Dependencies
├── .env                    # Konfigurasi (gitignored)
├── multibot.service        # systemd unit file
└── handlers/
    ├── start.py            # /start, /help
    ├── download.py         # /dl — video downloader
    ├── qr.py               # /qr — QR generator
    ├── shorten.py          # /short — URL shortener
    ├── sticker.py          # /sticker, /toimg
    ├── weather.py          # /cuaca — weather
    └── calc.py             # /calc — calculator
```

---

## 🛠 Tech Stack

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Telegram_Bot_API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  <img src="https://img.shields.io/badge/yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="yt-dlp">
  <img src="https://img.shields.io/badge/Pillow-512BD4?style=for-the-badge&logo=python&logoColor=white" alt="Pillow">
  <img src="https://img.shields.io/badge/systemd-E95420?style=for-the-badge&logo=linux&logoColor=white" alt="systemd">
</p>

---

## 🎨 Logo Gallery

<table align="center">
  <tr>
    <td align="center"><img src="assets/logo-v1-robot.png" width="128"><br><b>Robot</b><br><code>logo-v1-robot</code></td>
    <td align="center"><img src="assets/logo-v2-abstract.png" width="128"><br><b>Abstract</b><br><code>logo-v2-abstract</code></td>
    <td align="center"><img src="assets/logo-v3-monogram.png" width="128"><br><b>Monogram</b><br><code>logo-v3-monogram</code></td>
  </tr>
</table>

> 💡 Mau ganti logo? Generate pake AI prompt — rekomendasi: *"flat vector robot icon, two-tone dark purple + blue, clean geometric shapes, Catppuccin mocha palette, no gradients —Midjourney"*

---

<div align="center">
  <sub>v1.0 · 2026 · Built by <a href="https://github.com/mocasus">@mocasus</a></sub>
</div>
