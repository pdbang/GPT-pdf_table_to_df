from openai import OpenAI
import json
from io import StringIO
from pandas import DataFrame

def gpt_df_analysis(csv_data: StringIO, system_prompt: str, params_properties: dict, model: str = "gpt-3.5-turbo-1106") -> DataFrame:
    client = OpenAI()
    
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": csv_data.getvalue()}]

    tools = [{
        "type": "function",
        "function":{
        
            "name": "to_csv",
            "description": "Create a csv file with the given parameters",
            "parameters": params_properties
        }
    }]

    response = client.chat.completions.create(messages=messages,
                                   model=model,
                                   tool_choice={"type": "function", "function": {"name": "to_csv"}},
                                   tools=tools,
                                   temperature=0)
    print(response)
    arguments = response.choices[0].message.tool_calls[0].function.arguments
    print(arguments)
    return json.loads(arguments)


def gpt_cols_and_rows(df_data: DataFrame, system_prompt: str, model: str = "gpt-3.5-turbo-1106") -> (list, list):
    csv_data = StringIO()
    df_data.to_csv(csv_data)
    
    params_properties = {
        "type": "object",
        "properties": {
            "Columns": {
                "type": "string",
                "description": "list of columns names infered from the csv",
            },
            "Rows": {
                "type": "string",
                "description": "list of rows names infered from the csv"
            }
        },
        "required": ["Columns", "Rows"]
    }
    result = gpt_df_analysis(csv_data, system_prompt, params_properties, model)
    return result["Rows"], result["Columns"]

def gpt_df_from_cols(df_data: DataFrame, system_prompt: str, rows: list, cols: list, rows_desc: list=None, cols_desc: list=None, model: str = "gpt-3.5-turbo-1106") -> DataFrame:
    csv_data = StringIO()
    df_data.to_csv(csv_data)

    params_properties = {
        "type": "object",
        "properties": {
            f"{row} ## {col}": {
                "type": "string",
                "description": f"{rows_desc[i] or ''} ## {cols_desc[j] or ''}"
            } for (i, row) in enumerate(rows) for (j, col) in enumerate(cols)
        },
        "required": []
    }
    return gpt_df_analysis(csv_data, system_prompt, params_properties, model)