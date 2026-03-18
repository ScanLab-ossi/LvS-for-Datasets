# LVS for Datasets

A lightweight command-line workflow for running the **LvS (Learning via Surprisability)** algorithm on tabular datasets with:

- **two categorical dimensions**
- **one frequency / value column**
- optional **graph generation**
- configurable **signature extraction** and **top dynamic features**

---

## What this project does

The repository processes a CSV dataset, computes LvS-oriented outputs, and saves the results locally.

**Main entry point:** `main.py`

**Default output location:** `./results/{dataset}/lvs_results.csv`

---

## Quick start

### Run from the command line

You can either:

1. edit a `config.ini` file in advance, or
2. pass parameters directly in the Python command line.

### Example command

```bash
/opt/homebrew/bin/python3.11 /Documents/GitHub/LVS-FOR-DATASETS/main.py   --file_path /Documents/GitHub/LVS-FOR-DATASETS/demo.csv   --dataset market   --agg_column Industry   --entity_name Country   --value_name Marketcap   --output_path results/market/allrenamedlvs.csv   --output_dic results/market/dic.csv   --sig_file results/market/signatures.csv   --graph True   --top 5   --sig_length 70
```

### Same example in one line

```bash
/opt/homebrew/bin/python3.11 /Documents/GitHub/LVS-FOR-DATASETS/main.py --file_path /Documents/GitHub/LVS-FOR-DATASETS/demo.csv --dataset market --agg_column Industry --entity_name Country --value_name Marketcap --output_path results/market/allrenamedlvs.csv --output_dic results/market/dic.csv --sig_file results/market/signatures.csv --graph True --top 5 --sig_length 70
```

### With a config file

```bash
python3.11 LVS-FOR-DATASETS/main.py --config LVS-FOR-DATASETS/config.ini
```

---

## Command-line parameters

| Parameter | Required | Description |
|---|---:|---|
| `file_path` | Yes | Path to the main CSV input file. |
| `dataset` | Yes | Logical dataset name used for organizing outputs. |
| `agg_column` | Yes | First-level aggregation column, for example `Industry`. |
| `entity_name` | Yes | Second-level aggregation column, for example `Country`. |
| `value_name` | Yes | Numeric frequency/value column, for example `Marketcap`. |
| `output_path` | Yes | Output CSV path for processed LvS results. |
| `output_dic` | Yes | Output CSV path for the generated dictionary / mapping file. |
| `sig_file` | Yes | Output CSV path for signatures. |
| `graph` | No | `True` / `False` — whether to generate graphs. |
| `top` | No | Number of top dynamic features to keep. |
| `sig_length` | No | Signature length: number of element values in each signature. |
| `short_names` | No | Whether to encode long source values into shorter labels. |
| `config` | No | Path to `config.ini`. Useful when you prefer configuration-driven execution. |

---

## Expected input format

The input must be a CSV with:

- one aggregation column
- one entity column
- one numeric value column

### Example input

| Industry | Country | MarketCap |
|---|---|---:|
| Electricity | Brazil | 12 |
| Electricity | France | 14 |
| Retail | France | 28 |
| Retail | USA | 53 |
| Technology | USA | 93 |

---

## Output structure

A typical run creates files under the dataset results directory.

```text
results/
└── market/
    ├── allrenamedlvs.csv
    ├── dic.csv
    └── signatures.csv
```

Depending on your settings, graph files may also be created.

---

## Configuration file

The configuration is stored in `config.ini`.  
This file is optional because all parameters can also be supplied from the command line.

### Example `config.ini`

```ini
[data]
file_path = documents/demo/real.csv
dataset = market

[proc]
agg_column = Industry
entity_name = Country
value_name = Marketcap

[output]
output_path = results/real/lvs.csv
output_dic = results/real/dic.csv
sig_file = results/real/signatures.csv
graph = True
top = 5
sig_length = 70
short_names = False
```

---

## Configuration sections explained

### `[data]`
Defines the input source.

- `file_path`: CSV file path
- `dataset`: logical dataset name

### `[proc]`
Defines how the dataset is interpreted.

- `agg_column`: first grouping dimension
- `entity_name`: second grouping dimension
- `value_name`: numeric metric / frequency field

### `[output]`
Defines where results are stored and how much is generated.

- `output_path`: main LvS output file
- `output_dic`: dictionary / mapping output
- `sig_file`: signatures output
- `graph`: generate graphs or not
- `top`: number of top dynamic features
- `sig_length`: signature length
- `short_names`: shorten long labels

---

## Recommended workflow

1. Prepare a CSV with two dimensions and one numeric value column.
2. Decide whether you want to use direct CLI parameters or a config file.
3. Run `main.py`.
4. Inspect:
   - the processed LvS CSV
   - the dictionary file
   - the signatures file
   - generated graphs, if enabled

---

## Notes

- Keep column names consistent with the parameters you pass.
- Use `short_names=True` when labels are too long for readable output.
- Use `graph=True` when you want a visual inspection of expected vs. observed distributions and LvS markers.

---

## Example graph

Below is an example output graph generated by the project:

![Example LvS graph](LvS_Retail.png)

This kind of chart helps compare **expected** versus **observed** shares and highlights **LvS positive / negative signals** visually.
