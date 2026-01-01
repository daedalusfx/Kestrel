
# 🐦 Kestrel: Dukascopy Data Importer


**Kestrel** is a streamlined, resilient, and user-friendly desktop application designed to download historical market data from **Dukascopy** with ease.

Unlike the previous version, **Kestrel** focuses purely on file generation. It downloads data in **monthly chunks** to prevent timeouts on unstable connections and automatically **merges** them into a single, clean JSON file. No database setup required—just pure data.

---
![Preview](/screenshots/preview.png)
---

## 🚀 Key Features

* **🛡️ Smart Chunking Engine**
    Downloads data month-by-month. If your internet cuts out in December, you won't lose the data downloaded from January to November. The app retries failed chunks automatically.

* **🧩 Auto-Merge Capability**
    Once all monthly chunks are downloaded, Kestrel automatically merges them into one single JSON file and cleans up the temporary parts.
    * *Output Format:* `symbol-timeframe-bid-start-end.json`

* **🎨 Modern Catppuccin UI**
    Redesigned from the ground up with a soothing, professional dark theme (Catppuccin style) for better readability and a modern look.

* **🔒 Proxychains Support**
    Easily route your requests through **Proxychains** (or Tor) with a single checkbox to bypass censorship or firewalls.

* **📂 Organized Output**
    Automatically creates a `downloads` folder and saves your files there, keeping your workspace clean.

* **⚡ Lightweight & Fast**
    Stripped of heavy database dependencies (InfluxDB) and translation layers. It does one thing and does it well: fetching your data.

---

## 🐦 Why “Kestrel”?

Named after the **kestrel falcon**, known for its **precision** and ability to **hover** against the wind. This tool mirrors that stability: hovering through unstable network conditions to precisely capture the data you need.

---

## 📦 Requirements

Make sure the following are installed before running the app:

* **Python 3.x**
* **Node.js + npx** (Required for the core data fetching)
* **Python Dependencies:**
    ```bash
    pip install PyQt6 python-dateutil
    ```
* **Proxychains** (Optional, for censored networks)
    * Linux/Mac: `sudo apt install proxychains` (or via brew)

---

## ⚙️ Usage

### 1. Run the Application

```bash
python Kestrel.py

```

### 2. Configure Your Download

* **Symbol & Timeframe**: Select your desired instrument (e.g., `gbpaud`) and timeframe (e.g., `h1`).
* **Date Range**: Pick your Start and End dates.
* **Proxychains**: Check this box if you need to bypass internet restrictions.
* **Merge**: Keep this checked to get a single output file. Uncheck it if you prefer separate monthly files.

### 3. Start

Click **Start Download**. The app will:

1. Calculate the monthly chunks.
2. Download them one by one (displaying progress).
3. Merge them into a final file like: `gbpaud-h1-bid-2023-01-01-2023-12-20.json`.

---

## 🙏 Acknowledgments

🙏 Special thanks to **Leo**, the creator of the amazing [dukascopy-node](https://github.com/Leo4815162342/dukascopy-node) library — the backbone of Kestrel’s data-fetching engine.
Your contribution to the open-source community is deeply appreciated.




🙏 Dukascopy 🏦

A special thanks to **[Dukascopy Bank SA](https://www.dukascopy.com/)** for making high-quality financial market data **freely and transparently available** to the public.
This commitment to **data openness**, **market transparency**, and **freedom of access** is what empowers developers, researchers, and traders around the world to build better tools and gain deeper market insight.

This project is only possible because of Dukascopy’s forward-thinking philosophy. Thank you for supporting an open and informed financial ecosystem.



---

## 🪪 License

Kestrel is licensed under the **GNU General Public License v3.0**. See the `LICENSE` file for full details.

---

## ⚠️ Disclaimer

This software is provided **"as is"** for educational and research purposes. It is **not intended as financial advice**.
Always verify your data before making any investment decisions. Use at your own risk.

