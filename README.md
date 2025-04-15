# 🛡️ XSS_S – Advanced Multi-threaded XSS Scanner (Playwright + Firefox)

`xss_s` is a powerful and multithreaded XSS scanner designed for modern web applications. It uses Playwright with Firefox in headless mode to detect JavaScript alert popups triggered by XSS payloads. The tool supports concurrent scanning, WAF detection, and customizable headless operation.

## 🚀 Features

- ✅ Multi-threaded scanning for faster performance
- 🎯 Detects real JavaScript `alert()` popups
- 🔒 WAF detection (Cloudflare, Akamai, Sucuri, etc.)
- 🌐 Real browser interaction using Firefox (via Playwright)
- 🎨 Color-coded terminal output for clean visibility
- ⚙️ Toggle headless mode (visible or headless browser)
- 📁 Easy to use with `url.txt` and `payloads.txt`

---

## 📦 Requirements

Ensure the following are installed on your system:

### 🐍 Python 3.8+

Install required Python packages:

```bash
pip install -r requirements.txt

```bash
playwright install

### Usage
python3 Xss_s.py

