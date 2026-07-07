<p align="center">
  <img src="assets/logo-v1-robot.png" width="128" height="128" alt="MultiBot Logo">
</p>

<h3 align="center">🤖 MultiBot</h3>
<p align="center"><sub>Telegram multi-tool bot · inline UI · 9 modul handler · by <a href="https://github.com/mocasus">mmoaa</a></sub></p>

<p align="center">
  <a href="https://github.com/mocasus/multibot/releases"><img src="https://img.shields.io/badge/version-v2.0-181717?style=flat-square&logo=github" alt="Version"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square" alt="License"></a>
  <img src="https://img.shields.io/badge/python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/code%20style-ruff-30173D?style=flat-square&logo=ruff" alt="Ruff">
  <img src="https://img.shields.io/badge/handlers-9-4CAF50?style=flat-square" alt="Handlers">
</p>

<p align="center">
  <a href="https://github.com/mocasus/multibot/stargazers"><img src="https://img.shields.io/github/stars/mocasus/multibot?style=flat-square&cacheSeconds=86400" alt="Stars"></a>
  <a href="https://github.com/mocasus/multibot/network/members"><img src="https://img.shields.io/github/forks/mocasus/multibot?style=flat-square&cacheSeconds=86400" alt="Forks"></a>
  <a href="https://github.com/mocasus/multibot/issues"><img src="https://img.shields.io/github/issues/mocasus/multibot?style=flat-square&cacheSeconds=86400" alt="Issues"></a>
  <img src="https://img.shields.io/github/last-commit/mocasus/multibot?style=flat-square&cacheSeconds=86400" alt="Last Commit">
  <img src="https://img.shields.io/github/repo-size/mocasus/multibot?style=flat-square&cacheSeconds=86400" alt="Repo Size">
</p>

<p align="center">
  <a href="#-about"><img src="https://img.shields.io/badge/About-📖-brightgreen?style=flat-square" alt="About"></a>
  <a href="#-quick-start"><img src="https://img.shields.io/badge/Quick_Start-🚀-orange?style=flat-square" alt="Quick Start"></a>
  <a href="#-commands"><img src="https://img.shields.io/badge/Commands-📋-blue?style=flat-square" alt="Commands"></a>
  <a href="#-deploy"><img src="https://img.shields.io/badge/Deploy-🖥-red?style=flat-square" alt="Deploy"></a>
  <a href="#-project-structure"><img src="https://img.shields.io/badge/Structure-📁-gray?style=flat-square" alt="Structure"></a>
</p>

---

## 📖 About

**MultiBot** adalah bot Telegram serbaguna dengan antarmuka tombol inline (Bot API 10.1). Kirim perintah atau ketuk tombol — bot langsung proses. Dibangun di atas `python-telegram-bot` v22+ dengan arsitektur modular: 9 handler terpisah, masing-masing menangani satu domain fitur.

Bot ini support **rich message** (headings, tabel, collapsible `<details>`, styled buttons) via `sendRichMessage` API, serta fallback HTML untuk kompatibilitas penuh. Ideal buat bot utility, personal assistant, atau foundation buat bot yang lebih kompleks.

---

## ⚡ Quick Start

```bash
git clone https://github.com/mocasus/multibot.git && cd multibot
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
cp .env .env.local
# edit .env.local — isi BOT_TOKEN dari @BotFather
./venv/bin/python3 bot.py
```

<details>
<summary>📋 Output yang diharapkan</summary>

```
2026-07-08 INFO: Registered 10 handlers
2026-07-08 INFO: Bot mulai polling...
```
</details>

---

## 📋 Commands

| Command | Fungsi | Contoh |
|---------|--------|--------|
| `/start` | Welcome + menu inline (3 varian acak) | `/start` |
| `/help` | Panduan lengkap | `/help` |
| `/menu` | Menu utama | `/menu` |
| `/dl [url]` | Download video | `/dl https://instagram.com/p/...` |
| `/dlmp3 [url]` | Ekstrak audio MP3 | `/dlmp3 https://youtube.com/...` |
| `/qr [teks]` | Generate QR code | `/qr https://github.com` |
| `/short [url]` | Shorten URL (TinyURL/is.gd) | `/short https://example.com/long` |
| `/sticker` | Foto → Stiker (reply foto) | Reply foto + `/sticker` |
| `/toimg` | Stiker → PNG (reply stiker) | Reply stiker + `/toimg` |
| `/cuaca [kota]` | Cek cuaca real-time | `/cuaca Jakarta` |
| `/calc [ekspr]` | Kalkulator (math parser) | `/calc sqrt(144) + 2^3` |
| `/note [teks]` | Simpan catatan + timestamp | `/note ide startup besok` |

---

## ✨ Fitur

| Fitur | Detail |
|-------|--------|
| 🎬 **Downloader** | TikTok, IG, YT, X, FB, Reddit — MP4 & MP3 |
| 📝 **Notebook** | Simpan catatan `.txt` — multi-append + auto-timestamp |
| 🧮 **Kalkulator** | Parser matematika lengkap (sin, cos, sqrt, ln, etc) |
| 🔳 **QR Code** | Generate QR code, langsung kirim gambar |
| 🔗 **URL Shortener** | TinyURL & is.gd — auto-fallback |
| 🌤 **Cuaca** | Info cuaca real-time via OpenWeatherMap |
| 🖼 **Stiker** | Konversi foto ↔ stiker Telegram |
| 🎨 **Rich Welcome** | 3 varian welcome acak — headings, `<details>`, tabel |
| 🎯 **Styled Buttons** | Primary/success/danger style + copy-to-clipboard |

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

## ⚙ Environment

| Variable | Required | Default | Deskripsi |
|----------|----------|---------|-----------|
| `BOT_TOKEN` | ✅ | — | Token dari [@BotFather](https://t.me/BotFather) |
| `WEATHER_API_KEY` | ❌ | — | API key [OpenWeatherMap](https://openweathermap.org/api) (untuk `/cuaca`) |
| `ADMIN_IDS` | ❌ | — | Telegram user ID admin (pisah koma) |

---

## 📁 Project Structure

```
multibot/
├── bot.py                  # Entry point — build Application, register handlers
├── config.py               # Env loader (.env → typed constants)
├── requirements.txt        # python-telegram-bot, httpx, yt-dlp, pillow
├── .env                    # Konfigurasi (gitignored)
├── .env.example            # Template konfigurasi
├── Dockerfile              # Container deployment
├── multibot.service        # systemd unit file
└── handlers/
    ├── __init__.py
    ├── start.py            # /start (3 varian welcome), /help
    ├── rich.py             # sendRichMessage + btn helpers (Bot API 10.1)
    ├── menu.py             # Inline menu router + callback dispatcher
    ├── download.py         # /dl, /dlmp3 — video/audio downloader
    ├── notebook.py         # /note — simpan catatan .txt
    ├── qr.py               # /qr — QR code generator
    ├── shorten.py          # /short — URL shortener
    ├── weather.py          # /cuaca — weather info
    ├── calc.py             # /calc — math calculator
    └── sticker.py          # /sticker, /toimg — sticker ↔ photo
```

---

## 🛠 Tech Stack

Python 3.11+ · python-telegram-bot v22+ · httpx · yt-dlp · Pillow · OpenWeatherMap API · TinyURL API · systemd · Docker · Bot API 10.1 (rich messages + styled buttons)

---

## 🎨 Logo

<p align="center">
  <img src="assets/logo-v1-robot.png" width="96"><br>
  <sub><b>Style:</b> flat vector · two-tone · #2D1B69 + #667EEA</sub>
</p>

<details>
<summary>🎭 Variant</summary>

| Style | File |
|-------|------|
| Robot | `assets/logo-v1-robot.png` |
| Abstract | `assets/logo-v2-abstract.png` |
| Monogram | `assets/logo-v3-monogram.png` |

</details>

<details>
<summary>🤖 AI Generation Prompt</summary>

```
Two-tone flat vector app icon, dark purple #2D1B69 background,
blue #667EEA icon elements, clean geometric shapes.
NO gradients, NO glow, NO sparkle, NO 3D, NO text.
Rounded corners 80px, 400x400 canvas.
—style flat —ar 1:1
```
```
dua-tone flat vector icon bot Telegram, background ungu gelap
#2D1B69, elemen biru #667EEA, bentuk geometris bersih,
rounded corners, no shadow, no gradient, no text
```
</details>

---

<p align="center">
  <sub>v2.0 · 2026 · MIT License · Built by <a href="https://github.com/mocasus">mmoaa</a></sub>
</p>
