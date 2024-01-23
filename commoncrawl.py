from comcrawl import IndexClient
import pandas as pd

client = IndexClient(verbose=True)
client.search("https://arxiv.org/archive/q-fin/*", threads=16)

# client.results = (pd.DataFrame(client.results)
#                   .sort_values(by="timestamp")
#                   .drop_duplicates("urlkey", keep="last")
#                   .to_dict("records"))

client.download()

pd.DataFrame(client.results).to_csv("arxiv_quant_results.csv")