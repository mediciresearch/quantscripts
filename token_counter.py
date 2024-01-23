from transformers import BertTokenizer

# Initialize the tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Function to count the number of tokens using BERT's tokenizer
def count_tokens_bert(file_path, tokenizer):
    total_tokens = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            json_obj = json.loads(line)
            text = json_obj['text']
            # Tokenization using BERT's tokenizer
            tokens = tokenizer.tokenize(text)
            total_tokens += len(tokens)
    return total_tokens

# Call this function to get the total number of tokens with BERT's tokenizer
# total_token_count_bert = count_tokens_bert(output_jsonl_file, tokenizer)
# print(f"Total number of tokens in the dataset according to BERT's tokenizer: {total_token_count_bert}")
