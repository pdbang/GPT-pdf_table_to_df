from table_extraction.scripts import tables_utils, gpt_utils
import os

prompt_cols_base = "Ton objectif est de retrouver les noms de lignes et de colonnes adaptés dans ce csv qui est corrompu. Tu écriras les paramètres de la fonction sous forme de liste comme dans python : ['*nom*', '*nom*']."
prompt_values_base = "Tu dois interpréter le csv qui te sera donné par l'utilisateur pour choisir les valeurs pertinentes pour les paramètres de la fonction to_csv."

def basic_pdf_to_csv(filename: str, output_path):
    df = tables_utils.pdf_to_df(filename)
    df.to_csv(output_path)

def gpt_rows_and_cols(csv_file, openai_api_key : str, system_prompt: str):
    os.environ["OPENAI_API_KEY"] = openai_api_key
    system_prompt = prompt_cols_base + "\n" + system_prompt
    return gpt_utils.get_cols_and_rows(csv_file, system_prompt)

def gpt_csv_to_df(csv_file, openai_api_key: str, rows: list, cols: list, system_prompt: str):
    os.environ["OPENAI_API_KEY"] = openai_api_key
    system_prompt = prompt_values_base + "\n" + system_prompt
    dico = gpt_utils.get_csv_with_cols(csv_file, system_prompt, rows, cols)
    return tables_utils.to_csv(**dico)