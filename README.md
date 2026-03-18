# 📊 LvS for Datasets  
### Learning via Surprisability for Structured Data Analysis

![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)
![Research](https://img.shields.io/badge/research-HCI%20%7C%20Visualization-purple)
![CLI](https://img.shields.io/badge/interface-CLI-orange)

---

## 📑 Table of Contents
- [🔍 Overview](#-overview)
- [✨ What Makes This Different](#-what-makes-this-different)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Parameters](#️-parameters)
- [📂 Input Format](#-input-format)
- [📤 Output Structure](#-output-structure)
- [🧪 Example Visual Outputs](#-example-visual-outputs)
- [⚙️ Configuration File](#️-configuration-file)
- [🧠 Conceptual Background](#-conceptual-background)
- [📌 Notes](#-notes)
- [📄 License](#-license)

---

# 🔍 Overview

**LvS (Learning via Surprisability)** analyzes structured datasets by comparing:
- Expected distributions  
- Observed distributions  
- Surprise signals (LvS)

---

# ✨ What Makes This Different

- Models expectation vs reality gaps  
- Treats absence as signal  
- Aligns with human surprise perception  

---

# 🚀 Quick Start

```bash
python3 main.py --file_path demo.csv --dataset market --agg_column Industry --entity_name Country --value_name Marketcap --output_path results/market/lvs.csv --output_dic results/market/dic.csv --sig_file results/market/signatures.csv --graph True --top 5 --sig_length 70
```

---

# ⚙️ Parameters

| Parameter | Required | Description |
|----------|--------|------------|
| file_path | Yes | Input CSV |
| dataset | Yes | Dataset name |
| agg_column | Yes | Grouping column |
| entity_name | Yes | Entity column |
| value_name | Yes | Numeric column |

---

# 📂 Input Format

| Industry | Country | MarketCap |
|----------|--------|----------:|
| Retail | USA | 53 |

---

# 📤 Output Structure

results/
└── market/
    ├── lvs.csv
    ├── dic.csv
    └── signatures.csv

---

# 🧪 Example Visual Outputs

![Pharmaceuticals](LvS_Pharmaceuticals.png)
![Insurance](LvS_Insurance.png)
![Retail](LvS_Retail.png)
![Switzerland](LvS_Switzerland.png)

---

# ⚙️ Configuration File

```ini
[data]
file_path = demo.csv
dataset = market
```

---

# 🧠 Conceptual Background

Insight comes from deviations between expected and observed.

---

# 📄 License

MIT
