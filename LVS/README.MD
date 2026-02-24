# LVS

This repository contains the code for the LVS project.

# Default run (Command line) 
 LVS>  python3.11 ./data_process.py --config ./config_real.toml

## Input data 
* We accept 1 type of csv : freq - half processed data with frequencies 
For example : 

| Industry |Country | MarketCap|
|---|---|---|
|Electricity|Brazil|12|
|Electricity|France |14|
|Retail|France|28|
|Retail|USA|53| 
|Technology|USA|93| 

## Configuration

The configuration for the LVS project is stored in the `config_xxx.toml` [ xxx is the dataset name] file. This file is written in TOML format and contains the following sections:

### `[data]`

This section contains the configuration for the database. The following keys are supported:

* `file_path`: The input file of the dataset in csv format  [ ex - data/demo/demo.csv]
* `file_path2`: Optional : Additional input file with summary information [ None , or filename  ex - data/demo/population.csv]
* `dataset`: The dataset name [ex - demo] 
 
file_path  = data/demo/demo.csv
file_path2 = 
dataset = demo 

### `[proc]` 
This processing instructions
*  `agg_column` = Industry
*  `var_name` = Country
*  `value_name` = Marketcap
*  `processing_type` = freq 
*  `columns_to_remove` = E5,E6,E8  # columns that we like to remove from the original dataset 

### `[output]`
* `output_path` = results/cod/lvs.csv
* `output_dic` = results/cod/dic.csv 
* `sig_file` = results/cod/signatures.csv
* `graph` = [True/False] should we generate a graphs ? 
* `top` =  N top most dynamic features
* `sig_length` = length of signature (How many elements values in each signature) 
* `short_names` = False  # Do we like to encode long column names from the original dataset , with a shorter codes
### `constants` 
* `ignore_columns` = ['Entity','Code']
* `columns_to_keep` = ['document', 'element', 'frequency_in_document']  

Running full processing : data_process.py

| Parameter | Description |
|---|---|
| `file_path` | Path to the main CSV data file. |
| `file_path2` | Path to an optional secondary CSV file with summary information. |
| `dataset` | Name of the dataset. |
| `processing_type` | Specifies the type of processing: `full` for unpivoting and frequency calculation, or `freq` for frequency calculation only. |
| `agg_column` | Column used for aggregation (e.g., "Year"). |
| `var_name` | Name of the variable column (e.g., "Cause"). |
| `value_name` | Name of the value column (e.g., "Deaths"). |
| `output_path` | Path to the output CSV file containing processed data. |
| `output_dic` | Path to the output CSV file containing a dictionary or mapping. |
| `sig_file` | Path to the output CSV file for storing signatures. |
| `graph` | should we generate a graphs ?  |
| `top` | N top most dynamic features. |
| `sig_length` | length of signature (How many elements values in each signature) |
| `short_names`| Do we like to encode long column names from the original dataset , with a shorter codes|
| `columns_to_remove` |columns that we like to remove from the original dataset| # VisStudy
