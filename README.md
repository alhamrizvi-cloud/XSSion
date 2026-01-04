
# 🗡️ XSSion - Fastest XSS Reflection Finder
![GitHub stars](https://img.shields.io/github/stars/alhamrizvi-cloud/XSSion?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.x-blue?style=for-the-badge)
![License](https://img.shields.io/github/license/alhamrizvi-cloud/XSSion?style=for-the-badge)
![Bug Bounty](https://img.shields.io/badge/bug%20bounty-ready-red?style=for-the-badge)

XSSion is a fast, transparent **Reflected XSS scanning tool** designed for bug bounty hunters and penetration testers.  
It shows **every payload being tested in real time** and clearly highlights reflections in the response.

## 🧠 Description

- ⚡ Quickly finds reflected XSS vectors  
- 🎯 Shows **live testing** in terminal  
- 🔍 Automatically detects parameters (even blank ones like `?param=`)  
- 📌 Saves results to `XSSion.txt`  
- 🐍 Written in Python 3  
- 💥 Beginner friendly and bug bounty ready

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/alhamrizvi-cloud/XSSion.git
cd XSSion
````

Install dependencies:

```bash
pip3 install -r requirements.txt
```

## 📦 Make XSSion a Global Command

To run `xssion` from anywhere:

1. Add the shebang at the top if not present:

   ```python
   #!/usr/bin/env python3
   ```
2. Give execute permissions:

   ```bash
   chmod +x xssion.py
   ```
3. Move to a directory in your PATH:

   ```bash
   sudo mv xssion.py /usr/local/bin/xssion
   ```

Now you can run:

```bash
xssion <URL> <payloads.txt>
```

## 🚀 Usage

### Basic

```bash
python3 xssion.py "<URL>?param=" payloads.txt
```

Example:

```bash
xssion \
"https://www.bmw.de/de/shop/ls/cp/physical-goods/de-BF_ACCESSORY?tl=" \
xss_payloads.txt
```


## 📂 Example Payloads File

`xss_payloads.txt`:

```txt
"><svg/onload=alert(1)>
<script>alert(1)</script>
"><img src=x onerror=alert(1)>
```

## 📥 Output

Reflected payloads are saved to:

```
XSSion.txt
```

Example:

```
[XSS] https://target.com/search?q=<script>alert(1)</script> | <script>alert(1)</script>
```

## 📋 Features

* 🧪 Automatic parameter detection
* 🟡 Shows each payload tested
* 🔴 Highlights reflected ones
* 📊 Results logged to file


## 📈 Recommended Bug Bounty Workflow

```
gau / katana
   ↓
paramspider / arjun
   ↓
filter URLs with params
   ↓
XSSion
   ↓
dalfox / manual verification
```


## ⚠️ Notes

* XSSion finds **reflections**, try manual testing too if the parameter is vulnerable
* Some sites sanitize input or use client-side encoding
* Works best during early recon

## 🧪 Tested With

* Python 3.6+
* Linux & macOS


## 👨‍💻 Author

**Alham Rizvii** — Bug Bounty Hunter & Cybersecurity Enthusiast
Contributors are allowed

## 📜 License

This project is licensed under the **MIT License**.
See the `LICENSE` file for details.


