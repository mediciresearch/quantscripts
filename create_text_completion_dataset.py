import os
import json
from concurrent.futures import ThreadPoolExecutor
import threading

# Create a lock object
lock = threading.Lock()

# The single output JSONL file path
output_jsonl_file = "datasets/fin_books_large_paragraph_text_completion.jsonl"

import nltk
from nltk.tokenize import sent_tokenize

# Function to tokenize text into sentences and group into paragraphs
def text_to_paragraphs(text, max_sentences_per_paragraph=10):
    sentences = sent_tokenize(text)
    paragraphs = []
    current_paragraph = []

    for sentence in sentences:
        current_paragraph.append(sentence)
        if len(current_paragraph) >= max_sentences_per_paragraph:
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []
    
    # Add the last paragraph if there are any remaining sentences
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))

    return paragraphs

# Function to process a single file and write to the shared JSONL file
def process_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split the content by two newlines, assuming this denotes paragraphs
        paragraphs = text_to_paragraphs(content)
        
        # Convert paragraphs to JSONL format string
        jsonl_content = '\n'.join(json.dumps({"text": para}) for para in paragraphs)
        
        # Locking the thread to prevent other threads from entering this block
        with lock:
            with open(output_jsonl_file, 'a', encoding='utf-8') as f:
                f.write(jsonl_content + '\n')
        
        print(f"Processed {file_path} into {output_jsonl_file}")
        
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")

import hashlib

# Function to generate a hash for a JSON object
def hash_json_object(json_obj):
    # Convert the JSON object to a string and encode it to bytes
    json_str = json.dumps(json_obj, sort_keys=True)
    # Use hashlib to generate a hash from the JSON string
    return hashlib.md5(json_str.encode('utf-8')).hexdigest()

# Function to remove duplicate JSON objects from the file
def remove_duplicates(file_path):
    unique_objects = set()
    unique_lines = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            json_obj = json.loads(line)
            # Generate a hash for the JSON object
            obj_hash = hash_json_object(json_obj)
            # If the hash is not in the set, it's a new unique object
            if obj_hash not in unique_objects:
                unique_objects.add(obj_hash)
                unique_lines.append(line)

    # Rewrite the file with only unique JSON objects
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(unique_lines)

# # Directory where your .txt files are stored
# directory = "./nougat-textbook"

# # List of files to process
# files_to_process = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.txt')]

# # Number of threads to use (you can adjust this according to your machine's capabilities)
# num_threads = 4

# #download nltk punkt thingy
# nltk.download('punkt')

# # Process the files using threading
# with ThreadPoolExecutor(max_workers=num_threads) as executor:
#     executor.map(process_file, files_to_process)


remove_duplicates("datasets/fin_books_cleaned_large_paragraph_text_completion.jsonl")