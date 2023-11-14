from tabula import read_pdf
import pandas as pd
from collections import defaultdict

def pdf_to_df(pdf_path : str, n_row_min : int = 10) -> pd.DataFrame:
    dfs = read_pdf(pdf_path, pages="all")
    dfs = [df for df in dfs if df.shape[0] > n_row_min]
    if len(dfs) == 1:
        return dfs[0]
    else:
        print("WARNING : More than one table have been detected, they have been concatened.")
        return pd.concat(dfs)

def long_to_wide(dico: dict) -> dict:
    print(dico)
    rows = defaultdict(dict)
    for key, value in dico.items():
        rows[key.split(" ## ")[0]][key.split(" ## ")[1].replace("?", "")] = value
    print(rows)
    return dict(rows)

def to_csv(**kwargs) -> pd.DataFrame:
    dico = long_to_wide(kwargs)
    return pd.DataFrame(dico).T.replace('-', pd.NA)