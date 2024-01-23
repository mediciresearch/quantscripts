from openai import OpenAI
import openpyxl
from openpyxl.utils import get_column_letter
import random
import pandas as pd
import json

client = OpenAI()

def gen_input_data(output_json_path, excel_file_path):
    output_data = []
    with open(output_json_path, 'r') as file:
        output_data = json.load(file)

    for query in output_data:
        try:
            completion = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[
                    {"role": "system", "content": "You are obedient and direct assistant who listens to exactly what the user asks. You generate accurate detailed questions a user could have asked based on information given."},
                    {"role": "user", "content": "The following is some information: \n" + query["text"] +
                     "\n Analyze the given financial information and formulate a pertinent question that aligns with this information as a potential answer, focusing on economic principles, market trends, or financial analysis." +
                     "\nONLY return the question the user may have asked and nothing else. Do not format it with Markdown."
                     }
                ]
            )

            print(completion.choices[0].message.content)

            # Append data to JSONL file

        except Exception:
            print(Exception)
            pass


gen_input_data("./instructgen/final_combined_animation_data.json",
               "./master_finetune_datasheet.xlsx")
