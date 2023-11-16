[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://gptable.streamlit.app/)
# GPT-pdf_table_to_df

This repository aims to enhance the usage of Tabula for extracting tables from PDFs by incorporating GPT-3.5.

Usage Example:
```python
import gptable

openai_api_key = "xxx"
system_prompt_cols = "Columns are Values, Units, and Percentage. For rows, be sure to keep only the row names that meet specific conditions."
system_prompt_values = "Good luck!"
gptable.set_openai_api_key(openai_api_key)
df_data = gptable.basic_pdf_to_csv("pdf/technical_data.pdf")
rows, cols = gptable.gpt_rows_and_cols(df_data, system_prompt_cols)
df_final = gptable.gpt_csv_to_df(df_data, rows, cols, system_prompt_values, rows_desc, cols_desc)
```

## Installation

Use the following command to install the required packages:

```python
%pip install --upgrade git+https://github.com/pdbang/GPT-pdf_to_csv.git
```
Additionally, to use tabula, make sure to have Java installed. You can download it from [Java's official website](https://www.java.com/en/download/).
