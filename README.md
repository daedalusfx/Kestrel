
# 🐦 Kestrel: Dukascopy Data Importer

**Kestrel** is a modern, bilingual, and user-friendly desktop application designed to help you download historical market data from **Dukascopy** and import it directly into an **InfluxDB** database — all with a few clicks.

Whether you're a **financial analyst**, **quantitative trader**, or **developer**, Kestrel gives you full control over how and when to fetch your data — even in restricted network environments.

---
![Preview](/screenshots/preview.png)
---

## 🚀 Features

* **Modern Dark UI**
  Built with PyQt6 and styled with a sleek, distraction-free dark theme.

* **Bilingual Interface (English / فارسی)**
  Switch languages instantly with one click — fully localized UI and messages.

* **Flexible Download Modes**

  * **Latest Candles**: Retrieve a fixed number of recent bars (e.g., last 1000 H1 candles).
  * **Date Range**: Define exact start and end dates to get the data you need.

* **Direct Import to InfluxDB**
  Automatically parses the downloaded data and sends it to your InfluxDB instance — correctly timestamped and formatted.

* **Tor Proxy Support**
  One checkbox enables routing through the **Tor network**, bypassing censorship or firewalls in restricted regions.

* **Live Logging Panel**
  View real-time output of the data-fetching and database import process inside the application.

* **Configurable InfluxDB Settings**
  Input and save your InfluxDB **URL**, **Token**, **Organization**, and **Bucket** directly from the GUI.

* **Smart Error Handling**
  Detects and warns about empty or malformed JSON files before import — preventing silent data issues.

---

## 🐦 Why “Kestrel”?

Named after the **kestrel falcon**, known for its **precision**, **agility**, and the ability to **hover mid-air** before striking. These traits mirror the goals of this tool: precision in data, agility in access, and control in execution.

We hope this name also brings a little more attention to this beautiful bird of prey.

---

## 📦 Requirements

Make sure the following are installed before running the app:

* **Python 3.x**
* **PyQt6**
  Install with: `pip install PyQt6`
* **InfluxDB Python Client**
  Install with: `pip install influxdb-client`
* **Node.js + npx**
  Required to run `dukascopy-node`
* **Tor + Torsocks** (optional, for censored networks)
  Example for Debian/Ubuntu:
  `sudo apt update && sudo apt install tor torsocks`
* **InfluxDB 2.x or newer**
  A running instance accessible over HTTP.

---

## ⚙️ Setup & Usage

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd kestrel-importer
```

### 2. Install Dependencies

Ensure all components listed in the **Requirements** section are installed.

### 3. Run the Application

```bash
python main.py
```

### 4. Using the App

* **Configure InfluxDB**:
  Enter your connection details under the **Settings** tab. Values are saved automatically.

* **Set Download Parameters**:
  Choose your **symbol**, **timeframe**, and **download mode** (bars or date range).

* **Enable Tor (if needed)**:
  Check the "Use Tor Proxy" box if you’re in a restricted region.

* **Start Import**:
  Click “Start Download & Import” and watch the live logs as data flows in.

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

