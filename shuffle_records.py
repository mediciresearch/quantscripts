import json
import random

def shuffle_jsonl_file(input_file_path, output_file_path):
    # Read all lines/records into memory
    with open(input_file_path, 'r', encoding='utf-8') as f:
        records = f.readlines()
    
    # Shuffle the list of records
    random.shuffle(records)
    
    # Write the shuffled records to the new file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.writelines(records)

# Call this function with the path to your .jsonl file
shuffle_jsonl_file('datasets/FINLIT_RAW_TEXT_COMPLETION.jsonl', 'datasets/FINLIT_SHUFFLED_RAW_TEXT_COMPLETION.jsonl')
