# 🌙 **Blue Moon**

**Blue Moon** is a lightweight cryptocurrency dashboard built with **PySide6**.  
It fetches live market data from the **CoinGecko API** and provides a simple, intuitive interface for tracking the top 50 coins by market capitalization.  
The latest updates include improved CSV export behavior and bug fixes.  

---

## 📑 **Table of Contents**

- [❓ Why Blue Moon](#-why-blue-moon)  
- [✨ Features](#-features)  
- [🧰 Tech Stack](#-tech-stack)  
- [🎬 Demo](#-demo)  
- [🛠️ Requirements](#-requirements)  
- [📦 Installation](#-installation)  
- [🚀 Usage](#-usage)  
- [📁 CSV Export](#-csv-export)  
- [🗂️ Project Structure](#-project-structure)  
- [⚙️ Configuration & Settings](#-configuration--settings)  
- [🛣️ Roadmap](#-roadmap)  
- [🤝 Contributing](#-contributing)  
- [📜 License](#-license)  
- [📬 Contact](#-contact)  
- [🙏 Acknowledgments](#-acknowledgments)  

---

## ❓ **Why Blue Moon**

Tracking crypto markets often means juggling between multiple sites and APIs.  
**Blue Moon** was built to provide a **single lightweight desktop dashboard** with:

- ⚡ Real-time market data  
- 🔍 Integrated search & filtering  
- 📤 Exportable reports for analysis  
- 🎨 A clean and minimal UI  

---

## ✨ **Features**

- ⚡ Real-time data fetching for the **top 50 cryptocurrencies** by market cap.  
- 🖥️ Display of market data in a clean GUI powered by PySide6.  
- 🔍 Search / filter capability on the list of coins.  
- 📤 Export of current data to CSV with improved behavior in latest commit.  
- 🧩 Minimal dependencies; focuses on UX clarity.  

---

## 🧰 **Tech Stack**

- 🐍 **Python 3.8+**  
- 🖼️ **PySide6** – Modern Qt bindings for Python GUI  
- 🌐 **CoinGecko API** – Free crypto data provider  
- 📈 **Custom Graph Painter** – Chart rendering  
- 🎨 **QSS (Qt Stylesheets)** – Theming & styling  

---

## 🎬 **Demo**

![Blue Moon Demo](resources/demo.gif)

---

## 🛠️ **Requirements**

- 🐍 Python 3.8+ (or minimum tested version)  
- 🖼️ PySide6  
- 🌐 `requests` (or similar HTTP library)  
- 📡 Internet access for API requests to CoinGecko  

---

## 📦 **Installation**

1. **Clone the repository**

    ```bash
    git clone https://github.com/Ahmed-Ibrahim98/Blue_Moon.git
    cd Blue_Moon
    ```

2. **(Optional) Create a virtual environment**

    ```bash
    python3 -m venv venv
    source venv/bin/activate   # Linux / macOS
    venv\Scripts\activate      # Windows
    ```

3. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

    If no `requirements.txt` is provided, you’ll need at least:

    ```bash
    pip install PySide6 requests
    ```

4. **Run the application**

    ```bash
    python main.py
    ```

---

## 🚀 **Usage**

- On startup, Blue Moon shows the top 50 coins by market cap.  
- You can refresh the data (manual refresh) to get the latest.  
- Use search/filter to locate specific coins.  
- Click “Export CSV” to export current displayed data.  

---

## 📁 **CSV Export**

Example of exported data:

| Rank | Name (Symbol)     | Price (USD) | Market Cap   |
|------|-------------------|--------------|-------------|
| 1    | Bitcoin  (BTC)    | $65,000      | $1,2B      |
| 2    | Ethereum (ETH)    | $2,400       | $290M      |

👉 The exported CSV is saved in the working directory as:  
`crypto_data_<timestamp>.csv`  

---

## 🗂️ **Project Structure**

```plaintext
BLUE MOON/
├── main.py                 # Main entry point
├── resources/
│   ├── images/
│   │   ├── logo.png
│   │   ├── light.png
│   │   ├── dark.png
│   │   ├── refresh_light.png
│   │   └── refresh_dark.png
│   └── styles.qss          # Central stylesheet
└── app/
    ├── __init__.py
    ├── main_window.py      # Main application window 
    ├── config.py           # Constants and settings
    ├── api/
    │   ├── __init__.py
    │   └── coin_gecko.py   # API client 
    ├── logic/
    │   ├── __init__.py
    │   ├── data_controller.py # Business logic
    │   └── search_algorithm.py # Search Algorithm for the table data
    ├── utils/
    │   ├── __init__.py
    │   ├── formatting.py   # Data formatting helpers 
    │   ├── dialog.py       # Dialog for csv file saving 
    │   ├── file_saver.py   # Helper Class for saving csv files
    │   └── graph_painter.py # Custom graph drawing file to draw our charts
    └── views/
        ├── __init__.py
        ├── header_view.py      # Header widget 
        ├── table_view.py       # Table widget 
        ├── chart_view.py       # Chart widget 
        └── status_bar_view.py  # Status Bar Widget
```

---

## ⚙️ **Configuration & Settings**

- **API Endpoint:** Uses CoinGecko (free/public).  
  To use a different API, modify the data-fetching logic in `app/api/coin_gecko.py`.
- **CSV Export Directory:** By default, exports to the current working directory.  
  You can change this in the code or add a setting.

---

## 🛣️ **Roadmap**

- 🧪 Add unit tests.
- ⚙️ Support more customization (e.g., number of coins, selected currencies).
- 🗂️ Document more edge cases for CSV export.
- 🔁 Add auto-refresh feature.

---

## 🤝 **Contributing**

Thank you for your interest in improving Blue Moon!  
If you'd like to contribute:

1. **Fork** the repository.  
2. **Create a branch:**  
   `git checkout -b feature/your-feature-name`
3. **Make changes** with clear comments and docstrings.
4. **Test** your changes.
5. **Open a Pull Request** with a clear description.

---

## 📜 **License**

This project is licensed under the [MIT License].

---

## 📬 **Contact**

- **Author**: Ahmed Ibrahim  
- **GitHub**: [Ahmed-Ibrahim98 / Blue_Moon](https://github.com/Ahmed-Ibrahim98/Blue_Moon)  
- **Email**: *ahmedelmorsi990@gmail.com*

---

## 🙏 **Acknowledgments**

- CoinGecko for providing the API.  
- PySide6 for making GUI development more straightforward.  

---