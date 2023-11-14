from openai import OpenAI
import json
from io import StringIO

def gpt_df_analysis(csv_data: StringIO, system_prompt: str, params_properties: dict, model: str = "gpt-3.5-turbo-1106"):
    client = OpenAI()
    
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": csv_data.getvalue()}]

    tools = [{
        "type": "function",
        "function":{
        
            "name": "to_csv",
            "description": "Create a csv file from the given parameters",
            "parameters": params_properties
    }
    }
    ]

    response = client.chat.completions.create(messages=messages,
                                   model=model,
                                   tool_choice={"type": "function", "function": {"name": "to_csv"}},
                                   tools=tools,
                                   temperature=0)
    
    arguments = response.choices[0].message.tool_calls[0].function.arguments
    print(arguments)
    return json.loads(arguments)


def get_cols_and_rows(csv_data: str, system_prompt: str, model: str = "gpt-3.5-turbo-1106") -> (list, list):
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

def get_csv_with_cols(csv_data: str, system_prompt: str, rows: list, cols: list, model: str = "gpt-3.5-turbo-1106"):
    params_properties = {
        "type": "object",
        "properties": {
            f"{row} ## {col}": {
                "type": "string"
            } for row in rows for col in cols
        },
        "required": []
    }
    return gpt_df_analysis(csv_data, system_prompt, params_properties, model)