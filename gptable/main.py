from gptable.scripts import tables_utils, gpt_utils
import os
from pandas import DataFrame

prompt_cols_base = 'Ton objectif est de retrouver les noms de lignes et de colonnes adaptés dans ce csv qui est corrompu. Tu écriras les paramètres de la fonction sous forme de liste comme dans python : ["*nom*", "*nom*"].'
prompt_values_base = "Tu dois interpréter le csv qui te sera donné par l'utilisateur pour choisir les valeurs pertinentes pour les paramètres de la fonction to_csv."

def set_openai_api_key(openai_api_key: str):
    os.environ["OPENAI_API_KEY"] = openai_api_key

def basic_pdf_to_df(filename: str) -> DataFrame:
    df_data = tables_utils.pdf_to_df(filename)
    return df_data

def gpt_rows_and_cols(df_data, system_prompt: str) -> (list, list):
    system_prompt = prompt_cols_base + "\n" + system_prompt
    return gpt_utils.gpt_cols_and_rows(df_data, system_prompt)

def gpt_clean_df(df_data, rows: list, cols: list, system_prompt: str) -> DataFrame:
    system_prompt = prompt_values_base + "\n" + system_prompt
    dico = gpt_utils.gpt_df_from_cols(df_data, system_prompt, rows, cols)
    return tables_utils.to_csv(**dico)

def gpt_basic_pdf_to_df(filename: str, rows: list, cols: list, system_prompt: str) -> DataFrame:
    df_data = basic_pdf_to_df(filename)
    return gpt_clean_df(df_data, rows, cols, system_prompt)
