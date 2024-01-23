from huggingface_hub import HfApi, login
# login()
api = HfApi()
api.upload_file(
    path_or_fileobj="datasets\FINLIT_SHUFFLED_CLEANED_TEXT_COMPLETION.jsonl",
    path_in_repo="FINLIT_TEXT_COMPLETION.jsonl",
    repo_id="mediciresearch/finlit_text",
    repo_type="dataset",
)

# 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

# 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