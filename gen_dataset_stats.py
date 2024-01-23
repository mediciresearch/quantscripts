import os
import json
import numpy as np
from collections import Counter
import nltk
from nltk.corpus import stopwords

# Function to generate statistics from a .jsonl file
def generate_stats_file(input_jsonl_path, output_stats_path, top_n_tokens=10):

    #grab nltk stopwords
    nltk.download('stopwords')

    # Initialize counters
    num_records = 0
    num_characters = 0
    word_counter = Counter()
    record_lengths = []

    # Load stop words
    stop_words = set(stopwords.words('english'))

    # Process the .jsonl file
    with open(input_jsonl_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                json_obj = json.loads(line)
                text = json_obj.get('text', '')
                num_records += 1
                num_characters += len(text)
                # Tokenize and remove stop words
                words = [word for word in text.split() if word.lower() not in stop_words]
                word_counter.update(words)
                record_lengths.append(len(text))
            except json.JSONDecodeError:
                print(f"Invalid JSON in line: {line}")

    # Calculate additional statistics
    token_record_lengths = [length / 4 for length in record_lengths] 
    vocabulary_size = len(word_counter)
    average_tokens_per_record = (np.mean(token_record_lengths) if token_record_lengths else 0)
    max_record_length = (np.max(token_record_lengths) if token_record_lengths else 0) 
    min_record_length = (np.min(token_record_lengths) if token_record_lengths else 0) 
    num_tokens = num_characters / 4
    percentiles = np.percentile(token_record_lengths, [25, 50, 75]) if token_record_lengths else [0, 0, 0]
    common_words = word_counter.most_common(top_n_tokens)

    # Prepare the statistics table
    stats_table = f"""Statistics for {os.path.basename(input_jsonl_path)}
-------------------------------------------
File Name: {os.path.basename(input_jsonl_path)}
Number of Records: {num_records}
Number of Characters: {num_characters}
Number of Tokens: ~{num_tokens}
Vocabulary Size: {vocabulary_size}
Average Tokens per Record: {average_tokens_per_record:.2f}
Max Record Length (Tokens): {max_record_length}
Min Record Length (Tokens): {min_record_length}
25th Percentile Record Length (Tokens): {percentiles[0]}
50th Percentile Record Length (Median) (Tokens): {percentiles[1]}
75th Percentile Record Length (Tokens): {percentiles[2]}
Most Frequent Words (excluding common words): {', '.join([f'{word[0]} ({word[1]} times)' for word in common_words])}
"""

    # Write the statistics to the output text file
    with open(output_stats_path, 'w', encoding='utf-8') as output_file:
        output_file.write(stats_table)

    print(f"Statistics written to {output_stats_path}")

# Usage
generate_stats_file('datasets/FINLIT_SHUFFLED_CLEANED_TEXT_COMPLETION.jsonl', 'datasets/STATS_FINLIT_SHUFFLED_CLEANED.txt')
