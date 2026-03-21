#Always use 3.11.9 
#!/usr/bin/env python3
import argparse
import configparser
import os
import pandas as pd
import altair as alt
from LPA import Corpus
import lvs_per_document

alt.data_transformers.disable_max_rows()

def load_data(file_path):
    # read input csv data file and return as DataFrame
    try:
        df = pd.read_csv(file_path)
        print(f"Data successfully loaded from {file_path}")
        print(f"DataFrame shape: {df.shape}") 
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None  # Important: Return None on error
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    
def transform_names(df,agg_column,var_name,value_name):
    #Use generic names for the columns to make the code more flexible and reusable.
    print(agg_column,var_name,value_name)
    # cast dynamically
    df[agg_column] = df[agg_column].astype("string")  # keeps <NA> nicely
    df[var_name] = df[var_name].astype("string")  # keeps <NA> nicely
    df[value_name]=df[value_name].astype("float")
    # Rename
    df = df.rename(columns={agg_column: 'document',
                            var_name  : 'element',
                            value_name: 'frequency_in_document'}) 
    # keep only 3 columns in the dataframe 
    df = df[['document', 'element', 'frequency_in_document']]
    #df['element'] = df['element'].str.replace(r'[^\w\s]', '_', regex=True)  
    #df['document'] = df['document'].str.replace(r'[^\w\s]', '_', regex=True)  
    df["element"] = df["element"].str.replace("/", "_", regex=False)
    df["document"] = df["document"].str.replace("/", "_", regex=False)
    return df    
  
def clean_data(df,short_names, dataset):
    """Cleans the DataFrame (e.g., keep only relevant columns , handles missing values, data type conversions)."""
    if df is None:
        print("Error: Input DataFrame is None. Skipping clean_data.")
        return None, None
    try:
        #clean elements that always = 0 in all the documents 
        print("Cleaning data...")
        # Group by 'element' and sum the frequency across all documents
        non_zero_elements = df.groupby('element')['frequency_in_document'].sum()
        out_dir="results/"+dataset
        os.makedirs(out_dir, exist_ok=True)
        
        # save the zero elements to a file"results/{dataset}/zero_elements.csv"
        non_zero_elements[non_zero_elements == 0].to_csv(out_dir+"/zero_elements.csv")
        #save the non zero elements to a file
        non_zero_elements[non_zero_elements > 0].to_csv(f"results/{dataset}/non_zero_elements.csv")
        # Keep only elements with a non-zero total frequency
        non_zero_elements = non_zero_elements[non_zero_elements > 0].index
        # Filter the original DataFrame to keep only those elements
        filtered_df = df[df['element'].isin(non_zero_elements)]
        df= filtered_df
        df_cleaned = df.dropna()
        # Keep only the relevant columns
        entity_code_df = None
        # Shorten the element names
        unique_elements = df['element'].unique()
        if short_names=='True':
            element_to_code = { element: f'E{i}' for i,  element  in enumerate(unique_elements) }
        else:
            # Create a mapping from element names to codes
            element_to_code = {element: element for i, element in enumerate(unique_elements)}
            
        df_cleaned['element'] = df_cleaned['element'].map(element_to_code)  

        # Create a DataFrame from the dictionary
        entity_code_df = pd.DataFrame(list(element_to_code.items()), columns=['element_name', 'element']) 
        return df_cleaned, entity_code_df
    except KeyError as e:
        print(f"Error: Column not found: {e}. Check your 'columns_to_keep' parameter.")
        return None, None
    except Exception as e:
        print(f"Error during data cleaning: {e}")
        return None, None
    
def transform_names(df,agg_column,var_name,value_name):
    print(agg_column,var_name,value_name)
    # cast dynamically
    df[agg_column] = df[agg_column].astype("string")  # keeps <NA> nicely
    df[var_name] = df[var_name].astype("string")  # keeps <NA> nicely
    df[value_name]=df[value_name].astype("float")
    # Rename
    df = df.rename(columns={agg_column: 'document',
                            var_name  : 'element',
                            value_name: 'frequency_in_document'}) 
    # keep only 3 columns in the dataframe 
    df = df[['document', 'element', 'frequency_in_document']]
    return df   

def save_results(df,entity_code_df, output_path,output_dic):
    if df is None:
        print("Error: Input DataFrame is None. Skipping save_results.")
        return

    """Saves the processed DataFrames to a CSV file."""
    try: 
        print(f"Saving results to: {output_path} and {output_dic}")
        df.to_csv(output_path, index=False)  # Don't include the index
        print(f"Data successfully saved to {output_path}")

        if output_dic:
            #  Create a DataFrame from the dictionary and save it.  Important for consistent structure.
            entity_code_df.to_csv(output_dic, index=False)            
            print(f"Dictionary successfully saved to {output_path.replace('.csv', '_dict.csv')}")
    except Exception as e:
        print(f"Error saving results: {e}")
def generate_signatures(df, entity_code_df, sig_file, dataset,graph,top,sig_length,var_name,value_name):
    """
    Generates and saves document signatures, along with related analyses and visualizations.

    Args:
        df (pd.DataFrame): Input DataFrame containing document data.
        entity_code_df (pd.DataFrame, optional): DataFrame mapping entity codes to names.
        sig_file (str, optional): Path to save the signature DataFrame.
        dataset (str): Name of the dataset for output directory.
    """
    if df is None:
        print("Error: Input DataFrame is None. Skipping generate_signatures.")
        return

    try:
        # Create results directory if it doesn't exist
        os.makedirs(f"results/{dataset}", exist_ok=True)
        print (f"sig_file: {sig_file}, dataset: {dataset}, graph: {graph}, top: {top}, sig_length: {sig_length}, var_name: {var_name}, value_name: {value_name}")
        # aggregate lines in df 
        df = df.groupby(['document', 'element'])['frequency_in_document'].sum().reset_index()
        freq=df
        corpus = Corpus(df, "document", "element", "frequency_in_document")
        dvr = corpus.create_dvr(equally_weighted=True) # Create Document Vector Representation (DVR)
        dvr.to_csv(f"results/{dataset}/dvr.csv")
        top = int(top)
        sig_length = int(sig_length)

        sigs = corpus.create_signatures(distance="JSD",sig_length=sig_length, most_significant=top,prevalent=0.1) #Hagit check if this is the right distance

        #  Saving top N changed elements
        sigs[1].to_csv(f"results/{dataset}/top_{top}_most_changed.csv")
        sig = pd.DataFrame(sigs[1])

        # Rename columns based on entity_code_df if provided
        if entity_code_df is not None:
            entity_code_to_name = entity_code_df.set_index("element")["element_name"].to_dict()
            new_columns = [
                entity_code_to_name.get(col, col) for col in sig.columns
            ]  # Use get() for safety
            sig.columns = new_columns
            sig.to_csv(f"results/{dataset}/top_{top}_most_changed_real_names.csv")

        # Save signatures if sig_file is provided
        if sig_file:
            ndf = pd.DataFrame(sigs[0])
            ndf.to_csv(sig_file, index=True)
            print(f"Signatures successfully saved to {sig_file}")
            #save the signatures with real names
            if entity_code_df is not None:
                ndf.columns = [entity_code_to_name.get(col, col) for col in ndf.columns]
                ndf.to_csv(sig_file.replace('.csv', '_real_names.csv'), index=True)
                print(f"Signatures with real names successfully saved to {sig_file.replace('.csv', '_real_names.csv')}")
        else:
            print("No signature file provided, skipping signature saving.")

        # split the ndf DataFrame  to several dataframes   , by the column name   
        output_dir = f"results/{dataset}/split_dataframes"
        os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist 
        print("-" * 30)

        # Iterate over each row of the DataFrame using iterrows()
        # This method yields both the index and the row (as a Series)
        for index, row in ndf.iterrows():
            # Convert the row (which is a pandas Series) to a DataFrame
            # .to_frame() converts the Series to a DataFrame with the original Series index as the new DataFrame's index
            # We can provide a column name, for instance, using the original index
            
            row = row[row.notnull()]

            row_df = row.to_frame(name=f'row_{index}_data')
            # Pivot the result. For a single row DataFrame, transposing it achieves the desired pivoted effect.
            pivoted_df = row_df 


            # Define a unique filename for each new CSV file

            clean_index = str(index).replace("/", "_")  # Replace any slashes in the index to avoid file path issues
            file_name = os.path.join(output_dir, f'row_{clean_index}.csv') 
            
            print (f"Processing row {index} into {file_name} with data:\n{row_df}\n")    

            # If the DataFrame is empty after dropping NaN columns, skip saving
            if pivoted_df.empty:    
                print(f"Row {index} has no data to save, skipping.")
                continue    

            # Save the pivoted DataFrame to a new CSV file.
            # The column names from the original DataFrame will be preserved as the header.
            # Select rows where the second column (index 1) is not null

            pivoted_df = pivoted_df[pivoted_df.iloc[:, 0].notna()]
            pivoted_sorted_desc = pivoted_df.sort_values(by=pivoted_df.columns[0], ascending=False)
            pivoted_sorted_desc.to_csv(file_name, index=True)

            print(f"Saved pivoted data for row {index} to '{file_name}'") 

           # Save element list
        with open(f"results/{dataset}/list.txt", "w") as f:
            for item in sigs[0]:
                f.write(f"{item}\n")
        # save list into dataframe  
        df_list = pd.DataFrame(sigs[0])
        print(f"Element list saved to results/{dataset}/list.txt")
        print(df_list.columns)
        pivot_the_list = df_list.melt(var_name=var_name, value_name=value_name, ignore_index=False)
        pivot_the_list = pivot_the_list.reset_index().rename(columns={'index': 'document'})
        df_list = pivot_the_list.dropna().reset_index(drop=True)   
        df_list.to_csv(f"results/{dataset}/list.csv", index=True)
        print(f"Element list saved to results/{dataset}/list.csv")      

        # expected vs observed
        print("Columns in df_list:", df_list.columns.tolist())
        print("Columns in dvr:", dvr.columns.tolist()) 
        # Sockpuppet analysis
        freq['doc_total'] = freq.groupby('document')['frequency_in_document'].transform('sum')
        freq['freq_norm'] = freq['frequency_in_document'] / freq['doc_total']
        print(freq.head(10))
               
        if graph == True:
            df_observed=df_list 
            df_observed = df_observed.rename(columns={ 
                            var_name  : 'element_observed',
                            value_name: 'LvS'}) 
            
            df_merged = pd.merge(
            df_observed, 
            dvr, 
            left_on=['element_observed'],   # Columns in the first DF (sig)
            right_on=['element'],  # Columns in the second DF (dvr)
            how='outer'  , 
            suffixes=('_ob', '_expected')
            )
            df_merged = pd.merge(
            df_merged, 
            freq, 
            left_on= ['document','element_observed'],   # Columns in the first DF (sig)
            right_on=['document','element'],  # Columns in the second DF (dvr)
            how='outer'  , 
            suffixes=('', '_base')
            )
            df_merged = df_merged.rename(columns={ 
                            'element_ob'  : 'key',
                            'freq_norm'   : 'observed',
                            'global_weight': 'expected' }) 
            df_merged['gap_val']=df_merged['observed']-df_merged['expected']
            
            print (df_merged.head(10) )  
            docs = df_merged[['document']]
            print (df_merged.head(10) )  
            docs = df_merged[['document']]



            lvs_per_document.plot_document (df_merged,dataset,docs) 
            #lvs_per_country.plot_document  (df_merged,dataset,docs) 
            df_merged.to_csv(f"results/{dataset}/lvs_results.csv", index=False)
            docs.to_csv(f"results/{dataset}/docs.csv", index=False)


            # Top 10 distances chart
            try:
                top_changing = sig[sig.sum(0).abs().sort_values(ascending=False).head(10).index]
                chart = (
                    alt.Chart(
                        top_changing.reset_index()
                        .melt(id_vars="index")
                        .rename(
                            columns={
                                "index": "document",
                                "variable": "element",
                                "value": "Distance from expected",
                            }
                        )
                    )
                    .mark_line()
                    .encode(x="document:N", y="Distance from expected", color="element")
                    .properties(width=1200, height=300, title="")
                )
                chart.save(f"results/{dataset}/top_{top}_distances.png", scale_factor=4.0)
                print(f"Top {top} distances chart saved to results/{dataset}/top_{top}_distances.png")
            except Exception as e:
                print(f"Error generating or saving top {top} distances chart: {e}")


    except Exception as e:
        print(f"Failure in generate_signatures: {e}")
        return None




# Define the pipeline  
# Reuse the functions from the basic example
# clean_data, filter_data, calculate_summary, save_results

def     process_data(file_path,agg_column,var_name,value_name,output_path,output_dic,sig_file,dataset,graph,top,sig_length,short_names):
    """
    Pipeline function to load, unpivot, clean, and save data.

    Args:
        file_path (str): Path to the input CSV file. 
        agg_column (str): Column to aggregate by during unpivoting.
        var_name (str): (also called Entity_name)   for the variable column after unpivoting.
        value_name (str): Name for the value column after unpivoting.
        output_path (str): Path to save the processed CSV file.
        output_dic (dict, optional): Dictionary to save as a CSV file.
    """
    df = load_data(file_path) 
    if df is None:
        print("Pipeline aborted due to error in load_data.")
        return  # Stop the pipeline

    df_unpivoted = transform_names(df, agg_column, var_name, value_name)
    df=df_unpivoted
    if df_unpivoted is None:
        print("Pipeline aborted due to error in unpivot_data.")
        return
    
    df_cleaned ,entity_code_df = clean_data(df_unpivoted,short_names, dataset) 

    # print(df_cleaned  ) 
    if df_cleaned is None:
        print("Pipeline aborted due to error in clean_data.")  
        return
 
    save_results(df_cleaned,entity_code_df, output_path, output_dic)
    print("Pipeline execution complete!")

    print ("Generating signatures...")
    print (f"sig_file: {sig_file}, dataset: {dataset}, graph: {graph}, top: {top}, sig_length: {sig_length}, var_name: {var_name}, value_name: {value_name}")
    generate_signatures(df_cleaned,entity_code_df,sig_file,dataset,graph,top,sig_length,var_name,value_name)  
    print("signatures execution complete!")

import argparse
import configparser
import os


def str2bool(value):
    if isinstance(value, bool):
        return value
    value = value.lower()
    if value in {"true", "1", "yes", "y", "on"}:
        return True
    if value in {"false", "0", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean value: {value}")


def main():
    parser = argparse.ArgumentParser(description="CLI first, config as fallback")

    parser.add_argument("--config", default="config.ini", help="Path to config file")

    parser.add_argument("--file_path", help="Input file path")
    parser.add_argument("--dataset", help="Dataset name")
    parser.add_argument("--agg_column", help="Aggregation column")
    parser.add_argument("--entity_name", help="Entity name column")
    parser.add_argument("--value_name", help="Value column")

    parser.add_argument("--output_path", help="Output file path")
    parser.add_argument("--output_dic", help="Output dictionary path")
    parser.add_argument("--sig_file", help="Signature file path")

    parser.add_argument("--graph", type=str2bool, help="Whether to generate graph")
    parser.add_argument("--top", type=int, help="Number of top items to show")
    parser.add_argument("--sig_length", type=int, help="Signature length")
    parser.add_argument("--short_names", type=str2bool, help="Whether to use short names")

    args = parser.parse_args()

    # Read config if it exists
    config = configparser.ConfigParser()
    config_loaded = False
    if args.config and os.path.exists(args.config):
        config.read(args.config)
        config_loaded = True
        print(f"Config file loaded: {args.config}")
    else:
        print(f"No config file found at: {args.config}")

    def get_value(cli_value, section, key, fallback=None, value_type=str):
        """CLI overrides config; config fills missing values; otherwise fallback."""
        if cli_value is not None:
            return cli_value

        if config_loaded and config.has_section(section) and config.has_option(section, key):
            if value_type is bool:
                return config.getboolean(section, key)
            if value_type is int:
                return config.getint(section, key)
            return config.get(section, key)

        return fallback

    # Resolve values: CLI first, then config, then fallback
    file_path = get_value(args.file_path, "data", "file_path")
    dataset = get_value(args.dataset, "data", "dataset")
    agg_column = get_value(args.agg_column, "proc", "agg_column")
    entity_name = get_value(args.entity_name, "proc", "entity_name")
    value_name = get_value(args.value_name, "proc", "value_name")

    output_path = get_value(args.output_path, "output", "output_path")
    output_dic = get_value(args.output_dic, "output", "output_dic")
    sig_file = get_value(args.sig_file, "output", "sig_file")

    graph = get_value(args.graph, "output", "graph", fallback=False, value_type=bool)
    top = get_value(args.top, "output", "top", fallback=25, value_type=int)
    sig_length = get_value(args.sig_length, "output", "sig_length", fallback=200, value_type=int)
    short_names = get_value(args.short_names, "output", "short_names", fallback=False, value_type=bool)

    # Required fields check
    required = {
        "file_path": file_path,
        "dataset": dataset,
        "agg_column": agg_column,
        "entity_name": entity_name,
        "value_name": value_name,
        "output_path": output_path,
        "output_dic": output_dic,
        "sig_file": sig_file,
    }

    missing = [key for key, value in required.items() if value is None]
    if missing:
        raise ValueError(
            "Missing required parameters: "
            + ", ".join(missing)
            + ". Provide them via command line or config file."
        )

    print("=== VALUES ===")
    print(f"file_path: {file_path}")
    print(f"dataset: {dataset}")
    print(f"agg_column: {agg_column}")
    print(f"entity_name: {entity_name}")
    print(f"value_name: {value_name}")
    print(f"output_path: {output_path}")
    print(f"output_dic: {output_dic}")
    print(f"sig_file: {sig_file}")
    print(f"graph: {graph}")
    print(f"top: {top}")
    print(f"sig_length: {sig_length}")
    print(f"short_names: {short_names}")

    process_data(
        file_path,
        agg_column,
        entity_name,
        value_name,
        output_path,
        output_dic,
        sig_file,
        dataset,
        graph,
        top,
        sig_length,
        short_names,
    )


if __name__ == "__main__":
    main()