# LVS-FOR-DATASETS

This repository contains the code for the LVS-FOR-DATASETS  project.

# Default run (Command line) 
If your datafile name is real.csv , you can  edit in advance the configuration file [example : config.ini]   or provide the parameters in the command line of Python. 

The output is saved in your local directory , named ./results/{dataset}/lvs_results.csv

Running full processing : main.py

| Parameter | Description |
|---|---|
| `file_path` | Path to the main CSV data file. | summary information. |
| `dataset` | Name of the dataset. | 
| `agg_column` | Column used for 1st level of aggregation (e.g., "Year"). |
| `entity_name` |  Column used for 2nd level of aggregation  (e.g., "Cause"). |
| `value_name` | Name of the frequency value column (e.g., "Deaths"). |
| `output_path` | Path to the output CSV file containing processed data. |
| `output_dic` | Path to the output CSV file containing a dictionary or mapping. |
| `sig_file` | Path to the output CSV file for storing signatures. |
| `graph` | should we generate a graphs ?  |
| `top` | N top most dynamic features. |
| `sig_length` | length of signature (How many elements values in each signature) |
| `short_names`| Do we like to encode long column names from the original dataset , with a shorter codes| 


The command to execute the LvS algorithm is :

 LVS>  python3.11   LVS-FOR-DATASETS/main.py  | 
--file_path  /Users/demo.csv |
--dataset market |
--agg_column Industry |
--entity_name Country |
--value_name Marketcap |
--output_path results/market/allrenamedlvs.csv  |
--output_dic  results/market/dic |
--sig_file    results/market/signatures.csv |
--graph True |
--top 5  |
--sig_length 70  |
--config LVS-FOR-DATASETS/config.ini |

## in 1 line : 
/opt/homebrew/bin/python3.11 /Documents/GitHub/LVS-FOR-DATASETS/main.py   --file_path   /Documents/GitHub/LVS-FOR-DATASETS/demo.csv --dataset market --entity_name Country  --value_name Marketcap --output_path results/market/allrenamedlvs.csv  --output_dic results/market/dic --sig_file results/market/signatures.csv --graph True --top 5  --sig_length 70  --agg_column Industry

## Input data 
* We accept 1 type of csv : data with 2 dimensions and frequencies 
For example : 

| Industry |Country | MarketCap|
|---|---|---|
|Electricity|Brazil|12|
|Electricity|France |14|
|Retail|France|28|
|Retail|USA|53| 
|Technology|USA|93| 

## Configuration

The configuration for the LVS project is stored in the `config.ini` The file is optional , since tou can provide the parameters in the command line. This file  contains the following sections:

### `[data]`

This section contains the configuration for the database. The following keys are supported:

* `file_path`: The input file of the dataset in csv format  [ ex - documents/demo/real.csv] 
* `dataset`: The logical dataset name [ex - market] 
 
file_path  = documents/demo/real.csv]
dataset = market 

### `[proc]` 
This section contains the processing instructions
*  `agg_column` = Industry
*  `entity_name` = Country
*  `value_name` = Marketcap 

### `[output]`
This section contains the output files locations 

* `output_path` = results/real/lvs.csv
* `output_dic` = results/real/dic.csv 
* `sig_file` = results/real/signatures.csv
* `graph` = [True/False] should we generate a graphs ? 
* `top` =  N top most dynamic features
* `sig_length` = length of signature (How many elements values in each signature) 
* `short_names` = False  # Do we like to encode long column names from the original dataset , with a shorter codes 